<template>
  <div class="attendance-overview">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <div class="row mb-3">
            <div class="col-md-6">
              <h2>Attendance Overview</h2>
            </div>
            <div class="col-md-6 text-right">
              <button
                @click="showSendQrModal"
                class="btn btn-secondary mb-2 mr-2"
                :disabled="!selectedEvent"
                title="Select an event first"
              >
                Send QR Codes
              </button>
              <button @click="exportAttendanceData" class="btn btn-primary mb-2">
                Export Attendance Data (CSV)
              </button>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
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
                  <th>Status</th>
                  <th>Actions</th>
                  <th>Allergies</th>
                  <th class="hide-mobile">Email</th>
                  <th class="hide-mobile">Study</th>
                  <th class="hide-mobile">Year</th>
                  <th class="hide-mobile">Event</th>
                  <th class="hide-mobile">Check-in Time</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="participant in filteredParticipants" :key="participant.id">
                  <td>{{ participant.name }}</td>
                  <td>
                    <span
                      class="badge"
                      :class="participant.attended ? 'badge-success' : 'badge-warning'"
                    >
                      {{ participant.attended ? 'Attended' : 'Not Attended' }}
                    </span>
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
                  <td>{{ participant.allergies || '-' }}</td>
                  <td class="hide-mobile">{{ participant.email }}</td>
                  <td class="hide-mobile">{{ participant.study }}</td>
                  <td class="hide-mobile">{{ participant.year }}</td>
                  <td class="hide-mobile">{{ getEventName(participant.event) }}</td>
                  <td class="hide-mobile">
                    {{ participant.check_in_time ? formatDateTime(participant.check_in_time) : '-' }}
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
      </div>
    </div>

    <!-- Send QR Modal -->
    <div v-if="showQrModal" class="modal-overlay" @click.self="closeQrModal">
      <div class="modal-content">
        <div class="modal-header">
          <h5>Send QR Codes</h5>
          <button @click="closeQrModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="loadingQrPreview" class="text-center py-3">
            <div class="spinner-border" role="status">
              <span class="sr-only">Loading...</span>
            </div>
            <p class="mt-2">Loading preview...</p>
          </div>
          <div v-else-if="qrPreview">
            <p><strong>Event:</strong> {{ qrPreview.program_name }}</p>
            <p><strong>Confirmed participants:</strong> {{ qrPreview.total_confirmed }}</p>
            <p><strong>Already received QR:</strong> {{ qrPreview.already_sent_count }}</p>
            <p><strong>Will receive QR now:</strong> <span class="text-primary font-weight-bold">{{ qrPreview.pending_qr_count }}</span></p>

            <div v-if="qrPreview.pending_qr_count === 0" class="alert alert-info mt-3">
              All confirmed participants have already received their QR codes.
            </div>
            <div v-else class="alert alert-warning mt-3">
              This will send {{ qrPreview.pending_qr_count }} email(s). Are you sure?
            </div>
          </div>
          <div v-if="sendingQr" class="text-center py-3">
            <div class="spinner-border" role="status">
              <span class="sr-only">Sending...</span>
            </div>
            <p class="mt-2">Sending emails...</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeQrModal" class="btn btn-secondary" :disabled="sendingQr">Cancel</button>
          <button
            @click="sendQrEmails"
            class="btn btn-primary"
            :disabled="sendingQr || loadingQrPreview || !qrPreview || qrPreview.pending_qr_count === 0"
          >
            Send Emails
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AttendanceOverviewView',
  data () {
    return {
      participants: [],
      events: [],
      selectedEvent: '',
      checkingIn: false,
      showQrModal: false,
      loadingQrPreview: false,
      qrPreview: null,
      sendingQr: false
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
        this.fetchEvents()
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

    formatDateTime (dateString) {
      return new Date(dateString).toLocaleString()
    },

    exportAttendanceData () {
      // Create CSV data
      const csvData = [
        ['Name', 'Email', 'Study', 'Year', 'Event', 'Allergies', 'Attended', 'Check-in Time'],
        ...this.participants.map(p => [
          p.name,
          p.email,
          p.study,
          p.year,
          this.getEventName(p.event),
          p.allergies || '',
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

    async showSendQrModal () {
      if (!this.selectedEvent) {
        alert('Please select an event first')
        return
      }

      this.showQrModal = true
      this.loadingQrPreview = true
      this.qrPreview = null

      try {
        const response = await axios.get(
          `${process.env.VUE_APP_API_HOST}/api/participant/send_qr_preview/`,
          {
            params: { program_id: this.selectedEvent },
            headers: { 'Authorization': `Token ${this.$store.state.admin.token}` }
          }
        )
        this.qrPreview = response.data
      } catch (err) {
        console.error('Failed to load QR preview:', err)
        alert('Failed to load preview: ' + (err.response && err.response.data && err.response.data.message ? err.response.data.message : 'Unknown error'))
        this.showQrModal = false
      } finally {
        this.loadingQrPreview = false
      }
    },

    closeQrModal () {
      if (!this.sendingQr) {
        this.showQrModal = false
        this.qrPreview = null
      }
    },

    async sendQrEmails () {
      this.sendingQr = true

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_HOST}/api/participant/send_qr_emails/`,
          { program_id: this.selectedEvent },
          { headers: { 'Authorization': `Token ${this.$store.state.admin.token}` } }
        )

        const { sent, failed, errors } = response.data

        if (failed === 0) {
          alert(`Success! Sent ${sent} QR code email(s).`)
        } else {
          alert(`Sent ${sent} email(s), but ${failed} failed. Check console for details.`)
          console.error('QR email failures:', errors)
        }

        this.showQrModal = false
        // Refresh participants to update qr_email_sent status
        await this.fetchParticipants()
      } catch (err) {
        console.error('Failed to send QR emails:', err)
        alert('Failed to send emails: ' + (err.response && err.response.data && err.response.data.message ? err.response.data.message : 'Unknown error'))
      } finally {
        this.sendingQr = false
      }
    }
  }
}
</script>

<style scoped>
.attendance-overview {
  padding: 20px;
}

.table th {
  border-top: none;
}

.badge {
  font-size: 0.9em;
}

.card {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  /* Hide extra columns on mobile */
  .hide-mobile {
    display: none !important;
  }

  .attendance-overview {
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

  .table-responsive {
    font-size: 0.95em;
    margin: 0 !important;
    padding: 0 !important;
    border-radius: 8px !important;
    border-left: 0 !important;
    border-right: 0 !important;
    overflow-x: auto;
  }

  .table {
    margin: 0 !important;
    min-width: 100%;
  }

  .table th,
  .table td {
    padding: 12px 8px !important;
    white-space: nowrap;
  }

  /* Make columns wider */
  .table th:nth-child(1),
  .table td:nth-child(1) {
    min-width: 120px; /* Name */
  }

  .table th:nth-child(2),
  .table td:nth-child(2) {
    min-width: 100px; /* Status */
  }

  .table th:nth-child(3),
  .table td:nth-child(3) {
    min-width: 100px; /* Actions */
  }

  .table th:nth-child(4),
  .table td:nth-child(4) {
    min-width: 120px; /* Allergies */
  }

  .card {
    border-radius: 8px !important;
    margin: 10px !important;
    padding: 15px !important;
  }

  .form-group, .mb-3 {
    margin-left: 10px !important;
    margin-right: 10px !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  h2 {
    padding: 15px 15px 10px 15px !important;
    margin-bottom: 5px !important;
  }

  .badge {
    padding: 6px 10px;
    font-size: 0.85em;
  }

  .btn-sm {
    font-size: 0.85em;
    padding: 6px 12px;
    white-space: normal;
    min-width: 80px;
  }
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h5 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #dee2e6;
}
</style>
