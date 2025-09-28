<template>
  <b-modal
    :id="modalId"
    ref="modal"
    :title="header"
    @show="resetModal"
    @hidden="resetModal"
    @ok="handleOk"
    :cancel-title="$t('cancel')"
    :ok-title="$t('register')"
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
      <b-form-group :label="$t('inputFieldAllergies')" label-for="allergies-input">
        <b-form-input
          id="allergies-input"
          v-model="form.allergies"
          ref="allergiesInput"
          :placeholder="$t('placeholderAllergies')"
          :state="allergiesState"
        >
        </b-form-input>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProgramRegistrationModal',
  props: [
    'modalId',
    'header',
    'name'
  ],
  data () {
    return {
      form: {
        name: '',
        email: '',
        study: '',
        year: '',
        allergies: ''
      },
      nameState: null,
      emailState: null,
      studyState: null,
      yearState: null,
      allergiesState: null,
      emailInvalidFeedbackDefault: this.$t('inputFieldEmail') + ' ' + this.$t('is_required'),
      emailInvalidFeedbackString: this.emailInvalidFeedbackDefault,
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
  },
  methods: {
    checkFormValidity () {
      const valid = this.$refs.form.checkValidity()

      const nameValid = this.$refs.nameInput.checkValidity()
      const emailValid = this.$refs.emailInput.checkValidity()
      const studyValid = this.$refs.studyInput.checkValidity()
      const yearValid = this.$refs.yearInput.checkValidity()
      const allergiesValid = this.$refs.allergiesInput.checkValidity()

      this.nameState = nameValid
      this.emailState = emailValid
      this.studyState = studyValid
      this.yearState = yearValid
      this.allergiesState = allergiesValid

      return valid
    },
    resetModal () {
      this.form.name = ''
      this.form.email = ''
      this.form.study = ''
      this.form.year = ''
      this.form.allergies = ''

      this.nameState = null
      this.emailState = null
      this.studyState = null
      this.yearState = null
      this.allergiesState = null
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
      axios.post(
        process.env.VUE_APP_API_HOST + '/api/participant/',
        { event: this.$props.name, ...this.$data.form }
      )
        .then(() => {
          this.$bvModal.hide(this.modalId)

          this.$emit('registration-success')
        })
        .catch((e) => {
          if (e.response.data.message.includes('already registered')) {
            this.emailState = false
            this.emailInvalidFeedbackString = this.$t('already_registered')
          }
        })
    },
  }
}
</script>
