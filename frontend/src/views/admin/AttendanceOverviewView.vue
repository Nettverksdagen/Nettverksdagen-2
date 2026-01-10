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
      checkingIn: false
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
</style>
