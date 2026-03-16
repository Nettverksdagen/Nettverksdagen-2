<template>
  <div class="attendance-scanner">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <h2>QR Code Scanner</h2>

          <div class="qr-scanner-container">
            <!-- Camera Scanner -->
            <div class="camera-scanner mb-4">
              <div v-if="!cameraEnabled">
                <button @click="startCamera" class="btn btn-lg btn-primary">
                  <i class="fa fa-camera"></i> Start Camera Scanner
                </button>
                <p class="text-muted mt-2">
                  <small>Note: Camera access requires HTTPS in production</small>
                </p>
              </div>

              <div v-else class="camera-view">
                <stream-barcode-reader
                  @decode="onDecode"
                  @loaded="onLoaded"
                  @error="onError"
                  class="qr-stream"
                ></stream-barcode-reader>

                <div class="camera-controls mt-3">
                  <button @click="stopCamera" class="btn btn-danger">
                    <i class="fa fa-times"></i> Stop Camera
                  </button>
                </div>

                <div v-if="cameraError" class="alert alert-danger mt-3" role="alert">
                  <h6><i class="fa fa-exclamation-circle"></i> Camera Error</h6>
                  <p class="mb-2">{{ cameraError }}</p>
                  <button @click="startCamera" class="btn btn-sm btn-primary mt-2">
                    <i class="fa fa-refresh"></i> Retry
                  </button>
                </div>
              </div>
            </div>

            <div class="manual-input mt-4">
              <!-- Error message -->
              <div v-if="scanError" class="alert alert-danger">
                {{ scanError }}
              </div>

              <!-- Success message -->
              <div v-if="scanSuccess" class="alert alert-success">
                {{ scanSuccess }}
              </div>

              <!-- Participant info after scan -->
              <div v-if="scannedParticipant" class="participant-card mt-4">
                <div class="card">
                  <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Participant Information</h5>
                  </div>
                  <div class="card-body">
                    <!-- Action buttons at top -->
                    <div class="action-buttons mb-3">
                      <button
                        v-if="!scannedParticipant.attended"
                        @click="checkInScannedParticipant"
                        class="btn btn-success btn-lg btn-block"
                        :disabled="checkingIn"
                      >
                        {{ checkingIn ? 'Checking In...' : 'Check In' }}
                      </button>
                      <button
                        v-else
                        @click="undoCheckInScanned"
                        class="btn btn-warning btn-lg btn-block"
                        :disabled="checkingIn"
                      >
                        {{ checkingIn ? 'Processing...' : 'Undo Check-in' }}
                      </button>
                      <button @click="resetScanner" class="btn btn-outline-secondary btn-block mt-2">
                        Scan Another
                      </button>
                    </div>

                    <hr>

                    <!-- Participant details -->
                    <div class="row">
                      <div class="col-md-6">
                        <p><strong>Name:</strong> {{ scannedParticipant.name }}</p>
                        <p><strong>Email:</strong> {{ scannedParticipant.email }}</p>
                        <p><strong>Study:</strong> {{ scannedParticipant.study }}</p>
                      </div>
                      <div class="col-md-6">
                        <p><strong>Year:</strong> {{ scannedParticipant.year }}</p>
                        <p><strong>Event:</strong> {{ getEventName(scannedParticipant.event) }}</p>
                        <p>
                          <strong>Status:</strong>
                          <span
                            class="badge ml-2"
                            :class="scannedParticipant.attended ? 'badge-success' : 'badge-warning'"
                          >
                            {{ scannedParticipant.attended ? 'Already Checked In' : 'Not Checked In' }}
                          </span>
                        </p>
                      </div>
                    </div>
                    <div v-if="scannedParticipant.check_in_time" class="mt-2">
                      <p><strong>Check-in Time:</strong> {{ formatDateTime(scannedParticipant.check_in_time) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { StreamBarcodeReader } from 'vue-barcode-reader'
import axios from 'axios'

export default {
  name: 'AttendanceScannerView',
  components: {
    StreamBarcodeReader
  },
  data () {
    return {
      events: [],
      manualToken: '',
      scannedParticipant: null,
      scanError: null,
      scanSuccess: null,
      verifying: false,
      checkingIn: false,
      cameraEnabled: false,
      cameraError: null
    }
  },
  async mounted () {
    await this.fetchEvents()
  },
  methods: {
    async fetchEvents () {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/program/`)
        this.events = response.data
      } catch (err) {
        console.error('Failed to fetch events:', err)
      }
    },

    async verifyAndShowParticipant () {
      if (!this.manualToken.trim()) {
        this.scanError = 'Please enter a token'
        return
      }

      this.verifying = true
      this.scanError = null
      this.scanSuccess = null
      this.scannedParticipant = null

      try {
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/participant/verify/`, {
          params: { token: this.manualToken.trim() }
        })

        if (response.data.valid) {
          this.scannedParticipant = response.data.participant
          this.manualToken = '' // Clear input
        } else {
          this.scanError = 'Invalid token'
        }
      } catch (err) {
        this.scanError = 'Error verifying token: ' + (err.response && err.response.data && err.response.data.message ? err.response.data.message : 'Unknown error')
      } finally {
        this.verifying = false
      }
    },

    async checkInScannedParticipant () {
      if (!this.scannedParticipant) return

      this.checkingIn = true
      this.scanError = null
      this.scanSuccess = null

      try {
        const response = await axios.post(`${process.env.VUE_APP_API_HOST}/api/participant/checkin/`, {
          token: this.scannedParticipant.attendance_token
        }, {
          headers: {
            'Authorization': `Token ${this.$store.state.admin.token}`
          }
        })

        this.scannedParticipant = response.data.participant
        this.scanSuccess = `${this.scannedParticipant.name} checked in successfully!`

        // Auto-reset and restart camera after 2 seconds
        setTimeout(() => {
          this.resetScanner()
          this.startCamera()
        }, 2000)
      } catch (err) {
        this.scanError = 'Check-in failed: ' + (err.response && err.response.data && err.response.data.message ? err.response.data.message : 'Unknown error')
      } finally {
        this.checkingIn = false
      }
    },

    async undoCheckInScanned () {
      if (!this.scannedParticipant) return

      this.checkingIn = true
      this.scanError = null
      this.scanSuccess = null

      try {
        const response = await axios.post(`${process.env.VUE_APP_API_HOST}/api/participant/undo_checkin/`, {
          token: this.scannedParticipant.attendance_token
        }, {
          headers: {
            'Authorization': `Token ${this.$store.state.admin.token}`
          }
        })

        this.scannedParticipant = response.data.participant
        this.scanSuccess = `Check-in undone for ${this.scannedParticipant.name}`

        // Auto-reset and restart camera after 2 seconds
        setTimeout(() => {
          this.resetScanner()
          this.startCamera()
        }, 2000)
      } catch (err) {
        this.scanError = 'Undo failed: ' + (err.response && err.response.data && err.response.data.message ? err.response.data.message : 'Unknown error')
      } finally {
        this.checkingIn = false
      }
    },

    resetScanner () {
      this.scannedParticipant = null
      this.manualToken = ''
      this.scanError = null
      this.scanSuccess = null
      // Auto-restart camera
      this.startCamera()
      // Focus back on input
      this.$nextTick(() => {
        if (this.$refs.tokenInput) {
          this.$refs.tokenInput.focus()
        }
      })
    },

    startCamera () {
      // Check if getUserMedia is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        this.cameraError = 'Your browser does not support camera access. Please use a modern browser (Chrome, Firefox, Edge, Safari).'
        return
      }

      this.cameraEnabled = true
      this.cameraError = null
    },

    stopCamera () {
      this.cameraEnabled = false
      this.cameraError = null
    },

    async onDecode (result) {
      // Stop camera and process QR code
      this.stopCamera()

      // Set the token and verify
      this.manualToken = result
      await this.verifyAndShowParticipant()
    },

    onLoaded () {
      this.cameraError = null
    },

    onError (error) {
      console.error('Camera error:', error)
      this.handleCameraError(error)
    },

    handleCameraError (error) {
      this.stopCamera()

      // Detect specific error types and provide user-friendly messages
      if (error.name === 'NotAllowedError') {
        this.cameraError = 'Camera permission denied. Please allow camera access in your browser settings and click "Start Camera Scanner" again.'
      } else if (error.name === 'NotFoundError') {
        this.cameraError = 'No camera device found. Please ensure your device has a camera connected.'
      } else if (error.name === 'NotReadableError') {
        this.cameraError = 'Camera is already in use by another application. Please close it and try again.'
      } else if (error.name === 'SecurityError') {
        this.cameraError = 'Camera access denied for security reasons. Note: Camera access requires HTTPS in production.'
      } else if (error.name === 'TypeError') {
        this.cameraError = 'Camera not supported. HTTPS connection may be required for camera access.'
      } else {
        this.cameraError = `Camera error: ${error.message || 'Unknown error occurred'}`
      }
    },

    getEventName (eventId) {
      const event = this.events.find(e => e.id === eventId)
      return event ? event.header : 'Unknown Event'
    },

    formatDateTime (dateString) {
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style scoped>
.attendance-scanner {
  padding: 20px;
}

.qr-scanner-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.manual-input {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.manual-input .form-control {
  font-size: 16px;
  padding: 12px;
}

.manual-input .btn {
  padding: 12px 24px;
}

.badge {
  font-size: 0.9em;
}

.card {
  margin-bottom: 20px;
}

.participant-card .card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.participant-card .card-body p {
  margin-bottom: 0.5rem;
}

.participant-card .card-footer {
  background-color: #f8f9fa;
}

.camera-scanner {
  text-align: center;
}

.camera-view {
  max-width: 600px;
  margin: 0 auto;
}

.qr-stream {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  border: 3px solid #007bff;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.scanner-frame {
  width: 250px;
  height: 250px;
  border: 3px solid #00ff00;
  border-radius: 12px;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
}

.camera-controls {
  text-align: center;
}

.alert h6 {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.alert p {
  margin-bottom: 0;
}

.alert .btn {
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .attendance-scanner {
    padding: 0 !important;
    margin-left: -15px !important;
    margin-right: -15px !important;
  }

  .container-fluid {
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  .row {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  .col-12, .col-md-6 {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  .qr-scanner-container {
    padding: 5px !important;
    max-width: 100%;
  }

  .card {
    border-radius: 4px !important;
    margin: 5px !important;
    padding: 10px !important;
  }

  .manual-input {
    margin: 5px !important;
    padding: 10px !important;
  }

  .participant-card .card {
    margin: 5px !important;
    padding: 8px !important;
  }

  .participant-card .card-body {
    padding: 10px !important;
  }

  h2 {
    padding: 15px 15px 10px 15px !important;
    margin-bottom: 5px !important;
  }

  .badge {
    padding: 6px 10px;
    font-size: 0.85em;
  }

  .btn {
    font-size: 0.9em;
    padding: 10px 16px;
  }

  .btn-lg {
    font-size: 1rem;
    padding: 12px 20px;
  }

  .qr-stream {
    max-width: 100%;
    border-width: 2px;
  }

  .camera-view {
    max-width: 100%;
  }

  .participant-card .card-body .row {
    margin: 0 !important;
  }

  .participant-card .card-body .col-md-6 {
    padding: 0 5px !important;
    margin-bottom: 8px;
  }

  .participant-card .card-body p {
    margin-bottom: 0.3rem;
    font-size: 0.95rem;
  }

  .action-buttons {
    margin-bottom: 10px !important;
  }

  .action-buttons .btn {
    font-size: 1rem;
    padding: 12px;
  }
}
</style>
