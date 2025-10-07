<template>
  <div class="qr-scanner">
    <h3>QR Code Scanner for Attendance</h3>

    <!-- Camera stream -->
    <div v-if="!scannedData" class="scanner-container">
      <video ref="video" autoplay playsinline class="scanner-video"></video>
      <canvas ref="canvas" style="display: none;"></canvas>
      <div class="scanner-overlay">
        <div class="scanner-frame"></div>
      </div>
      <button @click="startScanning" v-if="!scanning" class="btn btn-primary">
        Start Scanner
      </button>
      <button @click="stopScanning" v-if="scanning" class="btn btn-secondary">
        Stop Scanner
      </button>
    </div>

    <!-- Manual input fallback -->
    <div class="manual-input mt-3">
      <h5>Manual Input</h5>
      <div class="input-group">
        <input
          v-model="manualToken"
          @keyup.enter="verifyToken"
          placeholder="Enter attendance token"
          class="form-control"
        />
        <div class="input-group-append">
          <button @click="verifyToken" class="btn btn-outline-primary">
            Verify
          </button>
        </div>
      </div>
    </div>

    <!-- Participant info display -->
    <div v-if="scannedData" class="participant-info mt-4">
      <div class="card">
        <div class="card-header">
          <h5>Participant Information</h5>
        </div>
        <div class="card-body">
          <p><strong>Name:</strong> {{ scannedData.name }}</p>
          <p><strong>Email:</strong> {{ scannedData.email }}</p>
          <p><strong>Study:</strong> {{ scannedData.study }}</p>
          <p><strong>Year:</strong> {{ scannedData.year }}</p>
          <p><strong>Event:</strong> {{ eventName }}</p>
          <p><strong>Status:</strong>
            <span :class="scannedData.attended ? 'text-success' : 'text-warning'">
              {{ scannedData.attended ? 'Already checked in' : 'Not checked in' }}
            </span>
          </p>
          <div v-if="scannedData.check_in_time">
            <p><strong>Check-in time:</strong> {{ formatDateTime(scannedData.check_in_time) }}</p>
          </div>
        </div>
        <div class="card-footer">
          <button
            @click="checkIn"
            :disabled="scannedData.attended || checkingIn"
            class="btn btn-success me-2"
          >
            {{ checkingIn ? 'Checking in...' : 'Check In' }}
          </button>
          <button @click="resetScanner" class="btn btn-outline-secondary">
            Scan Another
          </button>
        </div>
      </div>
    </div>

    <!-- Error display -->
    <div v-if="error" class="alert alert-danger mt-3">
      {{ error }}
    </div>

    <!-- Success message -->
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QRScanner',
  data() {
    return {
      scanning: false,
      scannedData: null,
      manualToken: '',
      error: null,
      successMessage: null,
      checkingIn: false,
      eventName: '',
      stream: null
    }
  },
  methods: {
    async startScanning() {
      try {
        this.error = null
        const constraints = {
          video: {
            facingMode: 'environment' // Use back camera on mobile
          }
        }

        this.stream = await navigator.mediaDevices.getUserMedia(constraints)
        this.$refs.video.srcObject = this.stream
        this.scanning = true

        // Start continuous scanning
        this.scanInterval = setInterval(() => {
          this.captureAndScan()
        }, 1000)

      } catch (err) {
        this.error = 'Camera access denied or not available'
        console.error('Camera error:', err)
      }
    },

    stopScanning() {
      this.scanning = false
      if (this.scanInterval) {
        clearInterval(this.scanInterval)
      }
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop())
      }
    },

    captureAndScan() {
      if (!this.scanning) return

      const video = this.$refs.video
      const canvas = this.$refs.canvas
      const context = canvas.getContext('2d')

      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      context.drawImage(video, 0, 0, canvas.width, canvas.height)

      try {
        // Use a QR code library like jsQR here
        // For now, we'll simulate QR detection
        // In a real implementation, you'd use:
        // const imageData = context.getImageData(0, 0, canvas.width, canvas.height)
        // const code = jsQR(imageData.data, imageData.width, imageData.height)

        // Placeholder for actual QR detection
        // if (code) {
        //   this.processQRCode(code.data)
        // }
      } catch (err) {
        console.error('QR scanning error:', err)
      }
    },

    async verifyToken() {
      if (!this.manualToken.trim()) {
        this.error = 'Please enter a token'
        return
      }

      try {
        this.error = null
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/participant/verify/`, {
          params: { token: this.manualToken.trim() }
        })

        if (response.data.valid) {
          this.scannedData = response.data.participant
          await this.fetchEventName(this.scannedData.event)
          this.stopScanning()
        } else {
          this.error = 'Invalid token'
        }
      } catch (err) {
        this.error = (err.response && err.response.data && err.response.data.message) ? err.response.data.message : 'Failed to verify token'
      }
    },

    async processQRCode(qrData) {
      try {
        this.error = null
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/participant/verify/`, {
          params: { token: qrData }
        })

        if (response.data.valid) {
          this.scannedData = response.data.participant
          await this.fetchEventName(this.scannedData.event)
          this.stopScanning()
        } else {
          this.error = 'Invalid QR code'
        }
      } catch (err) {
        this.error = (err.response && err.response.data && err.response.data.message) ? err.response.data.message : 'Failed to verify QR code'
      }
    },

    async fetchEventName(eventId) {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/program/${eventId}/`)
        this.eventName = response.data.header
      } catch (err) {
        this.eventName = 'Unknown Event'
      }
    },

    async checkIn() {
      if (!this.scannedData || this.scannedData.attended) return

      this.checkingIn = true
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_HOST}/api/participant/checkin/`, {
          token: this.scannedData.attendance_token
        }, {
          headers: {
            'Authorization': `Token ${this.$store.state.admin.token}`
          }
        })

        this.scannedData = response.data.participant
        this.successMessage = 'Check-in successful!'
        setTimeout(() => {
          this.successMessage = null
        }, 3000)

      } catch (err) {
        this.error = (err.response && err.response.data && err.response.data.message) ? err.response.data.message : 'Check-in failed'
      } finally {
        this.checkingIn = false
      }
    },

    resetScanner() {
      this.scannedData = null
      this.manualToken = ''
      this.error = null
      this.successMessage = null
      this.eventName = ''
    },

    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString()
    }
  },

  beforeUnmount() {
    this.stopScanning()
  }
}
</script>

<style scoped>
.qr-scanner {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.scanner-container {
  position: relative;
  text-align: center;
}

.scanner-video {
  width: 100%;
  max-width: 400px;
  height: auto;
  border: 2px solid #ddd;
  border-radius: 8px;
}

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.scanner-frame {
  width: 200px;
  height: 200px;
  border: 2px solid #007bff;
  border-radius: 8px;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.3);
}

.manual-input {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.participant-info {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.btn {
  margin: 5px;
}
</style>