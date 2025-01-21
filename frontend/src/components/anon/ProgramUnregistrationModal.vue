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
    <b-alert>
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
        code: '',
      },
      emailState: null,
      codeState: null,
      emailInvalidFeedbackDefault: this.$t('inputFieldEmail') + ' ' + this.$t('is_required'),
      emailInvalidFeedbackString: this.emailInvalidFeedbackDefault,
      codeInvalidFeedbackDefault: this.$t('inputFieldCode') + ' ' + this.$t('is_required'),
      codeInvalidFeedbackString: this.codeInvalidFeedbackDefault,
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
    },
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
      this.form.email = ''
      this.form.code = ''

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
      this.resetInvalidFeedback();
      
      if (!this.checkFormValidity()) {
        return
      }

      const participant = this.getParticipant()
      const code = this.$data.form.code

      axios.delete(process.env.VUE_APP_API_HOST + '/api/participant/' + participant.id + '/', { data: { code, } })
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
      axios.get(process.env.VUE_APP_API_HOST + '/api/participant/' +  participant.id + '/')
    },
    // destroy_participant: function (event) {
    //   let email = prompt('Vennligst skriv inn emailen din:')
    //   let participants = this.$store.state.participant.all
    //   let participant = participants.filter(par => par.email === email && par.event === event)[0]
    //   if (participant === undefined && email !== null) {
    //     alert('Fant ingen deltakere med denne epost-adressen på dette arrangementet.')
    //     return
    //   }
    //   axios.get(process.env.VUE_APP_API_HOST + '/api/participant/' +
    //     participant.id + '/').then(_ => {
    //     // Prompt user for code, and delete participant if input matches
    //     let retry = true
    //     while (retry) {
    //       let inputedCode = prompt('Vennligst skriv inn koden som ble sendt til ' + participant.email + '. Hvis du ikke mottar mailen, vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
    //       if (confirm('Er du sikker på at du vil melde av ' + participant.name + '?')) {
    //         axios.delete(process.env.VUE_APP_API_HOST + '/api/participant/' + participant.id + '/', {
    //           data: {
    //             code: inputedCode
    //           }
    //         }).then(_ => {
    //           alert(participant.name + ' er nå avmeldt.')
    //         }).catch(_ => {
    //           alert('Det oppsto en feil under avmeldingen. Er koden feil tro?')
    //         })
    //       }
    //       break
    //     }
    //   }).catch(_ => {
    //     alert('Det oppsto en feil under sendingen av avmeldingskoden. Vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
    //   })
    // },
  }
}
</script>
