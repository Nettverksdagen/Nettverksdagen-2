<template>
  <b-modal
    :id="modalId"
    ref="modal"
    :title="header"
    @show="resetModal"
    @hidden="resetModal"
    @ok="handleOk"
    :cancel-title="$t('cancel')"
    :ok-title="$t('destroypart')"
    centered
  >
    <b-alert
      :show="unregistrationCodeSentAlertCountDown"
      dismissible
      variant="success"
      @dismissed="unregistrationCodeSentAlertCountDown=0"
    >
      {{ $t('unregistration_code_sent') }}
    </b-alert>
    <b-form
      ref="form"
      @submit.stop.prevent="handleSubmit"
    >
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
      <b-form-group :label="$t('inputFieldCode')" label-for="code-input" :invalid-feedback="codeInvalidFeedback">
        <b-form-input
          id="code-input"
          v-model="form.code"
          required
          ref="codeInput"
          :placeholder="$t('placeholderCode')"
          :state="codeState"
        >
        </b-form-input>
      </b-form-group>
    </b-form>
    <p>Finner du ikke koden? <b-link @click="sendUnregistrationCode">Trykk her for å få sende den på nytt.</b-link></p>
  </b-modal>
</template>

<script>
// THIS WAS WRITTEN QUICKLY AND DIRTY AND SHOULD BE REFACTORED (as is the spirit of this website)
// This component can probably be merged with ProgramRegistrationModal into a more generic component or something

import axios from 'axios'

export default {
  name: 'ProgramUnregistrationModal',
  props: [
    'modalId',
    'header',
    'name'
  ],
  data () {
    return {
      form: {
        email: '',
        code: ''
      },
      emailState: null,
      codeState: null,
      emailInvalidFeedbackDefault: this.$t('inputFieldEmail') + ' ' + this.$t('is_required'),
      emailInvalidFeedbackString: this.emailInvalidFeedbackDefault,
      codeInvalidFeedbackDefault: this.$t('inputFieldCode') + ' ' + this.$t('is_required'),
      codeInvalidFeedbackString: this.codeInvalidFeedbackDefault,
      unregistrationCodeSentAlertCountDown: 0
    }
  },
  computed: {
    emailInvalidFeedback () {
      // Check for empty field
      if (this.form.email === '') {
        return this.emailInvalidFeedbackDefault
      }

      // Invalid email
      return this.emailInvalidFeedbackString
    },
    codeInvalidFeedback () {
      // Check for empty field
      if (this.form.code === '') {
        return this.codeInvalidFeedbackDefault
      }

      // Invalid code
      return this.codeInvalidFeedbackString
    }
  },
  mounted () {
    if (this.$route.query.unregister !== undefined) {
      this.$bvModal.show(this.modalId)
    }
  },
  methods: {
    checkFormValidity () {
      const valid = this.$refs.form.checkValidity()

      this.checkEmailValidity()

      // Only set code valid when response from server is recieved
      const codeValid = this.$refs.codeInput.checkValidity() && null
      this.codeState = codeValid

      return valid
    },
    checkEmailValidity () {
      const participant = this.getParticipant()

      const emailValid = this.$refs.emailInput.checkValidity() && (participant !== undefined)
      this.emailState = emailValid

      if (this.form.email !== '' && participant === undefined) {
        this.emailInvalidFeedbackString = this.$t('participant_not_found')
      }

      return emailValid
    },
    resetInvalidFeedback () {
      this.emailState = null
      this.codeState = null

      this.emailInvalidFeedbackString = this.emailInvalidFeedbackDefault
      this.codeInvalidFeedbackString = this.codeInvalidFeedbackDefault
    },
    resetModal () {
      this.form.email = this.$route.query.email || ''
      this.form.code = this.$route.query.code || ''

      this.emailState = null
      this.codeState = null
    },
    handleOk (bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault()
      // Trigger submit handler
      this.handleSubmit()
    },
    getParticipant () {
      const email = this.$data.form.email
      const eventId = this.$props.name

      const participants = this.$store.state.participant.all
      return participants.filter(par => par.email === email && par.event === eventId)[0]
    },
    async handleSubmit () {
      this.resetInvalidFeedback()

      if (!this.checkFormValidity()) {
        return
      }

      const participant = this.getParticipant()
      const code = this.$data.form.code

      axios.delete(process.env.VUE_APP_API_HOST + '/api/participant/' + participant.id + '/', { data: { code } })
        .then(_ => {
          this.$bvModal.hide(this.modalId)

          this.$emit('unregistration-success')
        })
        .catch((error) => {
          this.codeState = false

          this.codeInvalidFeedbackString = error.response.data.message === 'Invalid code'
            ? this.$t('unregistration_failure_code_invalid')
            : this.$t('unregistration_failure_unknown')
        })
    },
    sendUnregistrationCode () {
      this.resetInvalidFeedback()

      if (!this.checkEmailValidity()) {
        return
      }

      const participant = this.getParticipant()

      axios.get(process.env.VUE_APP_API_HOST + '/api/participant/' + participant.id + '/')
        .then(() => {
          this.showUnregistrationCodeSentAlert()
        })
    },
    showUnregistrationCodeSentAlert () {
      this.unregistrationCodeSentAlertCountDown = 15
    }
  }
}
</script>
