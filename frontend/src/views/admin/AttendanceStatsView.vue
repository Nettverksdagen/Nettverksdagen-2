<template>
  <div class="attendance-stats">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <h2>Attendance Statistics</h2>

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
                  <div v-else>
                    <p class="text-muted">No statistics available</p>
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
                  <button @click="refreshStats" class="btn btn-primary btn-block">
                    <i class="fa fa-refresh"></i> Refresh Statistics
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

                  <!-- Empty state -->
                  <div v-if="!stats.by_program || stats.by_program.length === 0" class="text-center py-4">
                    <p class="text-muted">No event statistics available</p>
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
import axios from 'axios'

export default {
  name: 'AttendanceStatsView',
  data () {
    return {
      stats: {
        overall: null,
        by_program: []
      }
    }
  },
  async mounted () {
    await this.fetchStats()
  },
  methods: {
    async fetchStats () {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_HOST}/api/participant/attendance_stats/`)
        this.stats = response.data
      } catch (err) {
        console.error('Failed to fetch stats:', err)
      }
    },

    async refreshStats () {
      await this.fetchStats()
    },

    getProgressBarClass (rate) {
      if (rate >= 80) return 'bg-success'
      if (rate >= 60) return 'bg-warning'
      return 'bg-danger'
    }
  }
}
</script>

<style scoped>
.attendance-stats {
  padding: 20px;
}

.progress {
  height: 20px;
}

.badge {
  font-size: 0.9em;
}

.card {
  margin-bottom: 20px;
}

.table th {
  border-top: none;
}

@media (max-width: 768px) {
  .attendance-stats {
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
    min-width: 120px;
  }

  .table th:nth-child(2),
  .table td:nth-child(2) {
    min-width: 100px;
  }

  .table th:nth-child(3),
  .table td:nth-child(3) {
    min-width: 80px;
  }

  .table th:nth-child(4),
  .table td:nth-child(4) {
    min-width: 100px;
  }

  .table th:nth-child(5),
  .table td:nth-child(5) {
    min-width: 150px;
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

  h5 {
    font-size: 1.1rem;
  }

  .badge {
    padding: 6px 10px;
    font-size: 0.85em;
  }

  .btn {
    font-size: 0.9em;
    padding: 10px 16px;
  }

  .btn-block {
    width: 100%;
  }

  .progress {
    height: 18px;
  }

  .d-flex.align-items-center {
    flex-wrap: wrap;
  }

  .d-flex.align-items-center .mr-2 {
    margin-right: 8px !important;
    min-width: 50px;
  }
}
</style>
