<template>
  <div class="attendance-admin">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <h2>Attendance Management</h2>

          <!-- Navigation tabs -->
          <ul class="nav nav-tabs mb-4">
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'scanner' }"
                @click="activeTab = 'scanner'"
                href="#"
              >
                QR Scanner
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'overview' }"
                @click="activeTab = 'overview'"
                href="#"
              >
                Attendance Overview
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'statistics' }"
                @click="activeTab = 'statistics'"
                href="#"
              >
                Statistics
              </a>
            </li>
          </ul>


          <!-- Tab content -->
          <div class="tab-content">
            <!-- QR Scanner tab -->
            <div v-if="activeTab === 'scanner'" class="tab-pane active">
              <div class="qr-scanner-container">
                <h3>QR Code Scanner</h3>
                <p class="text-muted">Camera-based QR scanning will be available soon.</p>

                <div class="manual-input mt-4">
                  <h5>Manual Token Input</h5>
                  <p class="text-muted">Enter attendance token manually for check-in</p>
                  <div class="input-group mb-3">
                    <input
                      v-model="manualToken"
                      @keyup.enter="verifyAndShowParticipant"
                      placeholder="Paste attendance token here"
                      class="form-control"
                      ref="tokenInput"
                    />
                    <div class="input-group-append">
                      <button @click="verifyAndShowParticipant" class="btn btn-primary" :disabled="verifying">
                        {{ verifying ? 'Verifying...' : 'Verify' }}
                      </button>
                    </div>
                  </div>

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
                      <div class="card-footer">
                        <button
                          v-if="!scannedParticipant.attended"
                          @click="checkInScannedParticipant"
                          class="btn btn-success"
                          :disabled="checkingIn"
                        >
                          {{ checkingIn ? 'Checking In...' : 'Check In' }}
                        </button>
                        <button
                          v-else
                          @click="undoCheckInScanned"
                          class="btn btn-warning"
                          :disabled="checkingIn"
                        >
                          {{ checkingIn ? 'Processing...' : 'Undo Check-in' }}
                        </button>
                        <button @click="resetScanner" class="btn btn-outline-secondary ml-2">
                          Scan Another
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Attendance Overview tab -->
            <div v-if="activeTab === 'overview'" class="tab-pane active">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h4>Attendance Overview</h4>
                </div>
                <div class="col-md-6 text-right">
                  <div class="form-group">
                    <label for="eventFilter">Filter by Event:</label>
                    <select v-model="selectedEvent" @change="filterParticipants" class="form-control">
                      <option value="">All Events</option>
                      <option v-for="event in events" :key="event.id" :value="event.id">
                        {{ event.header }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Participants table -->
              <div class="table-responsive">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Study</th>
                      <th>Year</th>
                      <th>Event</th>
                      <th>Status</th>
                      <th>Check-in Time</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="participant in filteredParticipants" :key="participant.id">
                      <td>{{ participant.name }}</td>
                      <td>{{ participant.email }}</td>
                      <td>{{ participant.study }}</td>
                      <td>{{ participant.year }}</td>
                      <td>{{ getEventName(participant.event) }}</td>
                      <td>
                        <span
                          class="badge"
                          :class="participant.attended ? 'badge-success' : 'badge-warning'"
                        >
                          {{ participant.attended ? 'Attended' : 'Not Attended' }}
                        </span>
                      </td>
                      <td>
                        {{ participant.check_in_time ? formatDateTime(participant.check_in_time) : '-' }}
                      </td>
                      <td>
                        <button
                          v-if="!participant.attended"
                          @click="manualCheckIn(participant)"
                          class="btn btn-sm btn-success"
                          :disabled="checkingIn"
                        >
                          Check In
                        </button>
                        <button
                          v-else
                          @click="undoCheckIn(participant)"
                          class="btn btn-sm btn-warning"
                          :disabled="checkingIn"
                        >
                          Undo Check-in
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Empty state -->
              <div v-if="filteredParticipants.length === 0" class="text-center py-4">
                <p class="text-muted">No participants found</p>
              </div>
            </div>

            <!-- Statistics tab -->
            <div v-if="activeTab === 'statistics'" class="tab-pane active">
              <div class="row">
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header">
                      <h5>Overall Statistics</h5>
                    </div>
                    <div class="card-body">
                      <div v-if="stats.overall">
                        <p><strong>Total Registered:</strong> {{ stats.overall.total_registered }}</p>
                        <p><strong>Attended:</strong> {{ stats.overall.attended }}</p>
                        <p><strong>Not Attended:</strong> {{ stats.overall.not_attended }}</p>
                        <p><strong>Attendance Rate:</strong> {{ stats.overall.attendance_rate.toFixed(1) }}%</p>

                        <!-- Progress bar -->
                        <div class="progress mt-3">
                          <div
                            class="progress-bar bg-success"
                            :style="{ width: stats.overall.attendance_rate + '%' }"
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header">
                      <h5>Quick Actions</h5>
                    </div>
                    <div class="card-body">
                      <button @click="exportAttendanceData" class="btn btn-primary mb-2">
                        Export Attendance Data
                      </button>
                      <br>
                      <button @click="refreshStats" class="btn btn-outline-secondary">
                        Refresh Statistics
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Per-event statistics -->
              <div class="row mt-4">
                <div class="col-12">
                  <div class="card">
                    <div class="card-header">
                      <h5>Statistics by Event</h5>
                    </div>
                    <div class="card-body">
                      <div class="table-responsive">
                        <table class="table">
                          <thead>
                            <tr>
                              <th>Event</th>
                              <th>Total Registered</th>
                              <th>Attended</th>
                              <th>Not Attended</th>
                              <th>Attendance Rate</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="eventStat in stats.by_program" :key="eventStat.program_id">
                              <td>{{ eventStat.program_name }}</td>
                              <td>{{ eventStat.total_registered }}</td>
                              <td>{{ eventStat.attended }}</td>
                              <td>{{ eventStat.not_attended }}</td>
                              <td>
                                <div class="d-flex align-items-center">
                                  <span class="mr-2">{{ eventStat.attendance_rate.toFixed(1) }}%</span>
                                  <div class="progress flex-grow-1" style="height: 20px;">
                                    <div
                                      class="progress-bar"
                                      :class="getProgressBarClass(eventStat.attendance_rate)"
                                      :style="{ width: eventStat.attendance_rate + '%' }"
                                    ></div>
                                  </div>
                                </div>
                              </td>
                            </tr>
                          </tbody>
                        </table>
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
  </div>
</template>

<script>
import QRScanner from '@/components/admin/QRScanner.vue'
import axios from 'axios'

export default {
  name: 'AttendanceAdminView',
  components: {
    QRScanner
  },
  data () {
    return {
      activeTab: 'scanner',
      participants: [],
      events: [],
      selectedEvent: '',
      stats: {
        overall: null,
        by_program: []
      },
      checkingIn: false,
      manualToken: '',
      scannedParticipant: null,
      scanError: null,
      scanSuccess: null,
      verifying: false
    }
  },
  computed: {
    filteredParticipants () {
      if (!this.selectedEvent) {
        return this.participants
      }
      return this.participants.filter(p => p.event === parseInt(this.selectedEvent))
    }
  },
  async mounted () {
    await this.fetchData()
  },
  methods: {
    async fetchData () {
      await Promise.all([
        this.fetchParticipants(),
        this.fetchEvents(),
        this.fetchStats()
      ])
    },

    async fetchParticipants () {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/participant/`)
        this.participants = response.data
      } catch (err) {
        console.error('Failed to fetch participants:', err)
      }
    },

    async fetchEvents () {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/program/`)
        this.events = response.data
      } catch (err) {
        console.error('Failed to fetch events:', err)
      }
    },

    async fetchStats () {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/participant/attendance_stats/`)
        this.stats = response.data
      } catch (err) {
        console.error('Failed to fetch stats:', err)
      }
    },

    async manualCheckIn (participant) {
      this.checkingIn = true
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_HOST}/api/participant/checkin/`, {
          token: participant.attendance_token
        }, {
          headers: {
            'Authorization': `Token ${this.$store.state.admin.token}`
          }
        })

        // Update local participant data
        const index = this.participants.findIndex(p => p.id === participant.id)
        if (index !== -1) {
          this.participants[index] = response.data.participant
        }

        await this.fetchStats()
      } catch (err) {
        console.error('Check-in failed:', err)
        alert('Check-in failed: ' + (err.response && err.response.data && err.response.data.message ? err.response.data.message : 'Unknown error'))
      } finally {
        this.checkingIn = false
      }
    },

    async undoCheckIn (participant) {
      this.checkingIn = true
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_HOST}/api/participant/undo_checkin/`, {
          token: participant.attendance_token
        }, {
          headers: {
            'Authorization': `Token ${this.$store.state.admin.token}`
          }
        })

        // Update local participant data
        const index = this.participants.findIndex(p => p.id === participant.id)
        if (index !== -1) {
          this.participants[index] = response.data.participant
        }

        await this.fetchStats()
      } catch (err) {
        console.error('Undo check-in failed:', err)
        alert('Undo check-in failed: ' + (err.response && err.response.data && err.response.data.message ? err.response.data.message : 'Unknown error'))
      } finally {
        this.checkingIn = false
      }
    },

    filterParticipants () {
      // Computed property handles this
    },

    getEventName (eventId) {
      const event = this.events.find(e => e.id === eventId)
      return event ? event.header : 'Unknown Event'
    },

    getProgressBarClass (rate) {
      if (rate >= 80) return 'bg-success'
      if (rate >= 60) return 'bg-warning'
      return 'bg-danger'
    },

    formatDateTime (dateString) {
      return new Date(dateString).toLocaleString()
    },

    async refreshStats () {
      await this.fetchStats()
    },

    exportAttendanceData () {
      // Create CSV data
      const csvData = [
        ['Name', 'Email', 'Study', 'Year', 'Event', 'Attended', 'Check-in Time'],
        ...this.participants.map(p => [
          p.name,
          p.email,
          p.study,
          p.year,
          this.getEventName(p.event),
          p.attended ? 'Yes' : 'No',
          p.check_in_time ? this.formatDateTime(p.check_in_time) : ''
        ])
      ]

      const csvContent = csvData.map(row => row.join(',')).join('\n')
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)

      const a = document.createElement('a')
      a.href = url
      a.download = `attendance_data_${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
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

        // Refresh data
        await this.fetchData()

        // Auto-reset after 2 seconds
        setTimeout(() => {
          this.resetScanner()
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

        // Refresh data
        await this.fetchData()

        // Auto-reset after 2 seconds
        setTimeout(() => {
          this.resetScanner()
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
      // Focus back on input
      this.$nextTick(() => {
        if (this.$refs.tokenInput) {
          this.$refs.tokenInput.focus()
        }
      })
    }
  }
}
</script>

<style scoped>
.attendance-admin {
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

.progress {
  height: 20px;
}

.badge {
  font-size: 0.9em;
}

.nav-tabs .nav-link {
  cursor: pointer;
}

.tab-pane {
  padding-top: 20px;
  display: block;
}

.tab-pane.active {
  display: block;
}

.card {
  margin-bottom: 20px;
}

.table th {
  border-top: none;
}

.participant-card .card {
  border: 2px solid #007bff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.participant-card .card-body p {
  margin-bottom: 0.5rem;
}

.participant-card .card-footer {
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .table-responsive {
    font-size: 0.9em;
  }

  .btn-sm {
    font-size: 0.8em;
    padding: 0.25rem 0.5rem;
  }
}
</style>