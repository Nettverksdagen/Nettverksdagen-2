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

      <div v-if="registration">
        <!-- <div v-else>
          <p>{{ registrationStatusText }}</p>
        </div> -->
        <b-button v-if="enableRegistration" variant="primary" v-b-modal="'registrationModal' + name">
          {{ $t('register') }}
        </b-button>
        <b-button v-else disabled variant="secondary">
          {{ $t('registrationNotYetAvailable') }}
        </b-button>

        <b-button v-if="cancelEmail" variant="outline-primary" v-b-modal="'unregistrationModal' + name">{{$t('destroypart')}}</b-button>
      </div>
    </div>

    <ProgramRegistrationModal
      :modalId="'registrationModal' + name"
      :header="header"
      :name="name"
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

import ProgramRegistrationModal from '@/components/anon/ProgramRegistrationModal.vue';
import ProgramUnregistrationModal from './ProgramUnregistrationModal.vue';

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
    'cancelEmail',
    'registrationStart',
    'registrationEnd',
    'name'
  ],
  components: {
    ProgramRegistrationModal,
    ProgramUnregistrationModal,
  },
  data () {
    return {
      registrationSuccessAlertCountDown: 0,
      unregistrationSuccessAlertCountDown: 0,
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
      return new Date(date).toLocaleDateString()
    },
    showRegistrationSuccessAlert () {
      this.registrationSuccessAlertCountDown = 15
    },
    showUnregistrationSuccessAlert () {
      this.unregistrationSuccessAlertCountDown = 15
    },
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

</style>
