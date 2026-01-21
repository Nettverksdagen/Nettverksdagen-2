<template>
  <div class="event-container">
    <!-- Alert for registration success -->
    <b-alert
      :show="registrationSuccessAlertCountDown"
      dismissible
      variant="success"
      @dismissed="registrationSuccessAlertCountDown=0"
    >
      {{ $t('registration_success') }}
    </b-alert>

    <!-- Alert for unregistration success -->
    <b-alert
      :show="unregistrationSuccessAlertCountDown"
      dismissible
      variant="success"
      @dismissed="unregistrationSuccessAlertCountDown=0"
    >
      {{ $t('unregistration_success') }}
    </b-alert>

    <!-- Description -->
    <div class="event-card">
      <div class="event-header">
        <h1 class="event-title">{{ header }}</h1>
        <div class="event-timing">
          <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="icon"/>
          <span>{{ formatTime(timeStart) }} - {{ formatTime(timeEnd) }}</span>
        </div>
        <div v-if="place" class="event-place">
          <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="icon"/>
          <span>{{ place }} </span>
        </div>
      </div>

      <div class="event-body">
        <p v-if="Array.isArray(paragraph)" v-for="(paragraph, index) in paragraph" :key="index" class="event-description">
          {{ paragraph }}
        </p>
        <p v-else-if="paragraph" class="event-description">
          {{ paragraph }}
        </p>
      </div>

      <div v-if="registration" class="registration-section">
        <!-- Registration Status -->
        <div v-if="isRegistrationOpen" class="registration-stats">
          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-label">{{ $t('registered') }}</span>
              <span class="stat-value">{{ actual_participants() }} / {{ maxRegistered }}</span>
            </div>
            <div v-if="waiting_list_participants() > 0" class="stat-item waiting-list">
              <span class="stat-label">{{ $t('waiting_list') }}</span>
              <span class="stat-value">{{ waiting_list_participants() }}</span>
            </div>
            <div v-else class="stat-item available">
              <span class="stat-label">{{ $t('spotsAvailable') }}</span>
              <span class="stat-value">{{ maxRegistered - actual_participants() }}</span>
            </div>
          </div>
        </div>
        <div v-else class="registration-status-text">
          <p>{{ registrationStatusText }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="button-group">
          <template v-if="actual_participants() < maxRegistered">
            <button v-if="enableRegistration" class="btn-register" v-b-modal="'registrationModal' + name">
              {{ $t('register') }}
            </button>
            <button v-else disabled class="btn-register btn-disabled">
              {{ $t('registrationNotYetAvailable') }}
            </button>
          </template>

          <button v-if="allowDeregistration && enableRegistration" class="btn-unregister" v-b-modal="'unregistrationModal' + name">
            {{ $t('destroypart') }}
          </button>
        </div>
      </div>
    </div>

    <ProgramRegistrationModal
      :modalId="'registrationModal' + name"
      :header="header"
      :name="name"
      :allowDeregistration="allowDeregistration"
      @registration-success="showRegistrationSuccessAlert"
    />

    <ProgramUnregistrationModal
      :modalId="'unregistrationModal' + name"
      :header="header"
      :name="name"
      @unregistration-success="showUnregistrationSuccessAlert"
    />

  </div>
</template>

<script>

import ProgramRegistrationModal from '@/components/anon/ProgramRegistrationModal.vue'
import ProgramUnregistrationModal from './ProgramUnregistrationModal.vue'

export default {
  name: 'ProgramDescription',
  props: [
    'timeStart',
    'timeEnd',
    'place',
    'header',
    'paragraph',
    'registration',
    'maxRegistered',
    'allowDeregistration',
    'registrationStart',
    'registrationEnd',
    'name'
  ],
  components: {
    ProgramRegistrationModal,
    ProgramUnregistrationModal
  },
  data () {
    return {
      registrationSuccessAlertCountDown: 0,
      unregistrationSuccessAlertCountDown: 0
    }
  },
  computed: {
    isRegistrationOpen () {
      const now = new Date()
      return now >= new Date(this.registrationStart) && now <= new Date(this.registrationEnd)
    },
    enableRegistration () {
      return this.isRegistrationOpen
    },
    registrationStatusText () {
      const now = new Date()
      if (now < new Date(this.registrationStart)) {
        return `${this.$t('registrationOpensAt')} ${this.formatDate(this.registrationStart)}`
      }
      if (now > new Date(this.registrationEnd)) {
        return this.$t('registrationClosed')
      }
      return this.$t('waitlistAvailable')
    }

  },
  methods: {
    registered: function () {
      return this.$store.state.participant.all.filter(par => par.event === this.$props.name).length
    },
    actual_participants: function () {
      return Math.min(this.$store.state.participant.all.filter(par => par.event === this.$props.name).length, this.maxRegistered)
    },
    waiting_list_participants: function () {
      return Math.max(this.$store.state.participant.all.filter(par => par.event === this.$props.name).length - this.maxRegistered, 0)
    },
    formatTime (time) {
      return new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    formatDate (date) {
      const d = new Date(date)
      const day = d.getDate()
      const month = d.toLocaleDateString('nb-NO', { month: 'long' })
      const time = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      return `${day}. ${month} kl. ${time}`
    },
    showRegistrationSuccessAlert () {
      this.registrationSuccessAlertCountDown = 15
    },
    showUnregistrationSuccessAlert () {
      this.unregistrationSuccessAlertCountDown = 15
    }
  }
}
</script>

<style scoped>
.event-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  flex: 1;
  height: fit-content;

  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border: 1px solid #ddd;
  padding: 16px;

  /* max-height: 400px; */

  * {
    margin: 0;
  }
}
.event-card {
  /* overflow: scroll;
  overscroll-behavior: contain; */

  display: flex;
  flex-direction: column;
  /* justify-content: space-between; */
  gap: 20px;
}
.event-header {
  /* position: sticky;
  top: 0; */
  background: white;
}
.event-title {
  font-size: 2rem;
  font-weight: bold;
  text-align: left;
}
.event-timing, .event-place {
  font-size: 16px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;

  .icon {
    margin: 0 !important;
    width: 16px;
    height: 16px;
  }
}
.event-body {
  flex: 1;
  width: 100%;

  margin: 0;
}
.event-place {
  display: flex;
  align-items: center;
}
.event-place .icon {
  margin-right: 8px;
}

/* Registration Section */
.registration-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 8px;
}

.registration-stats {
  background: linear-gradient(135deg, #14403c 0%, #1d4844 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
}

.stats-row {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 120px;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1;
}

.stat-item.waiting-list {
  border-left: 2px solid rgba(255, 255, 255, 0.3);
  padding-left: 24px;
}

.stat-item.available {
  border-left: 2px solid rgba(255, 255, 255, 0.3);
  padding-left: 24px;
}

.registration-status-text {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 12px 16px;
  text-align: center;
  color: #666;
  font-weight: 500;
}

/* Button Group */
.button-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-register, .btn-unregister {
  flex: 0 1 auto;
  min-width: 100px;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  white-space: nowrap;
}

.btn-register {
  background: linear-gradient(135deg, #2c5f7c 0%, #3a7a9a 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(44, 95, 124, 0.2);
}

.btn-register:hover:not(.btn-disabled) {
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(44, 95, 124, 0.3);
  background: linear-gradient(135deg, #376d8c 0%, #4589ab 100%);
}

.btn-register:active:not(.btn-disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(44, 95, 124, 0.2);
}

.btn-disabled {
  background: #ccc;
  color: #666;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-unregister {
  background: white;
  color: #2c5f7c;
  border: 1.5px solid #2c5f7c;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.btn-unregister:hover {
  background: #2c5f7c;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(44, 95, 124, 0.25);
}

.btn-unregister:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(44, 95, 124, 0.2);
}

@media (max-width: 576px) {
  .stats-row {
    flex-direction: column;
    gap: 16px;
  }

  .stat-item.waiting-list,
  .stat-item.available {
    border-left: none;
    border-top: 2px solid rgba(255, 255, 255, 0.3);
    padding-left: 0;
    padding-top: 16px;
  }

  .button-group {
    flex-direction: column;
  }

  .btn-register, .btn-unregister {
    width: 100%;
  }
}

</style>
