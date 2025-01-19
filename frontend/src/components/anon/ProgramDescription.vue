<template>
  <div class="event-container">
    <!-- Alert for registration success -->
    <b-alert
      :show="registrationCountDown"
      dismissible
      variant="success"
      @dismissed="registrationCountDown=0"
    >
      {{ $t('registration_success') }}
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

      <div v-if="registration && cancelEmail">
        <div>{{$t('destroypart')}} <a href="mailto:admin@nettverksdagene.no">admin@nettverksdagene.no</a>.</div>
        <!-- Removed temporaraly until unregistration works securely. <b-link @click.native="destroy_participant(name)">{{$t('destroypart')}}</b-link> -->
      </div>

      <div v-if="registration" class="event-registration">
        <!-- <div v-else>
          <p>{{ registrationStatusText }}</p>
        </div> -->
        <b-button v-if="enableRegistration" variant="primary" v-b-modal="'dialogForm' + name">
          {{ $t('register') }}
        </b-button>
        <b-button v-else disabled variant="secondary">
          {{ $t('registrationNotYetAvailable') }}
        </b-button>
      </div>
    </div>

    <b-modal
      :id="'dialogForm' + name"
      ref="modal"
      :title="header"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
      centered
    >
      <b-form
        ref="form"
        @submit.stop.prevent="handleSubmit"
      >
        <b-form-group :label="$t('inputfieldName')" label-for="name-input" :invalid-feedback="$t('inputfieldName') + ' ' + $t('is_required')">
          <b-form-input
            id="name-input"
            v-model="form.name"
            required
            ref="nameInput"
            :placeholder="$t('placeholderName')"
            :state="nameState"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group :label="$t('inputFieldEmail')" label-for="email-input" :invalid-feedback="emailInvalidFeedback">
          <b-form-input
            id="email-input"
            type="email"
            v-model="form.email"
            required
            ref="emailInput"
            :placeholder="$t('placeholderEmail')"
            :state="emailState"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group :label="$t('inputFieldFieldOfStudy')" label-for="study-input" :invalid-feedback="$t('inputFieldFieldOfStudy') + ' ' + $t('is_required')">
          <b-form-input
            id="study-input"
            v-model="form.study"
            required
            ref="studyInput"
            :placeholder="$t('placeholderFieldOfStudy')"
            :state="studyState"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group :label="$t('inputFieldStudyYear')" label-for="year-input" :invalid-feedback="$t('inputFieldStudyYear') + ' ' + $t('is_required')">
          <b-form-input
            id="year-input"
            v-model="form.year"
            required
            ref="yearInput"
            :placeholder="$t('placeholderStudyYear')"
            :state="yearState"
          >
          </b-form-input>
        </b-form-group>
        <!-- <b-button variant="outline-secondary" @click="cancelForm">{{ $t('cancel') }}</b-button>
        <b-button variant="primary" type="submit">{{ $t('submit') }}</b-button> -->
        <!-- <template #modal-footer>
        </template> -->
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

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
  data () {
    return {
      form: {
        name: '',
        email: '',
        study: '',
        year: ''
      },
      nameState: null,
      emailState: null,
      studyState: null,
      yearState: null,
      emailInvalidFeedbackDefault: this.$t('inputFieldEmail') + ' ' + this.$t('is_required'),
      emailInvalidFeedbackString: this.emailInvalidFeedbackDefault,
      registrationCountDown: 0
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

    checkFormValidity () {
      const valid = this.$refs.form.checkValidity()

      const nameValid = this.$refs.nameInput.checkValidity()
      const emailValid = this.$refs.emailInput.checkValidity()
      const studyValid = this.$refs.studyInput.checkValidity()
      const yearValid = this.$refs.yearInput.checkValidity()

      this.nameState = nameValid
      this.emailState = emailValid
      this.studyState = studyValid
      this.yearState = yearValid

      return valid
    },
    resetModal () {
      this.form.name = ''
      this.form.email = ''
      this.form.study = ''
      this.form.year = ''

      this.nameState = null
      this.emailState = null
      this.studyState = null
      this.yearState = null
    },
    handleOk (bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault()
      // Trigger submit handler
      this.handleSubmit()
    },
    async handleSubmit () {
      // Exit when the form isn't valid
      this.emailInvalidFeedbackString = this.emailInvalidFeedbackDefault
      if (!this.checkFormValidity()) {
        return
      }

      // Create random unregister code
      this.form.code = Array(6).fill(0).map(x => Math.random().toString(36).charAt(2)).join('').toUpperCase()

      // Submit
      console.log({event: this.$props.name, ...this.$data.form})
      axios.post(process.env.VUE_APP_API_HOST +
        '/api/participant/', {event: this.$props.name, ...this.$data.form})
        .then((response) => {
          // console.log(response)
          this.$bvModal.hide('dialogForm' + this.$props.name)

          // Update registered count
          // this.registered += 1 // Doesn't work, since the count is not updated in the backend
          // alert(this.$t('registrationSuccess'))
          this.showSuccessAlert()
        })
        .catch((e) => {
          // console.log('Error in submitForm')
          // console.log(e)
          // console.log(e.response.data.message)

          // Set email state invalid, with message already registered
          if (e.response.data.message.includes('already registered')) {
            this.emailState = false
            this.emailInvalidFeedbackString = this.$t('already_registered')
          }
        })
    },

    showSuccessAlert () {
      this.registrationCountDown = 15
    },
    emailInvalidFeedback () {
      // Check for empty field
      if (this.form.email === '') {
        return this.emailInvalidFeedbackDefault
      }

      // Invalid email
      return this.emailInvalidFeedbackString
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

</style>
