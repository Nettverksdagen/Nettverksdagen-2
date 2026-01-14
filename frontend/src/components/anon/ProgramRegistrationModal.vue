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
      <b-form-group :label="$t('inputFieldFieldOfStudy')" label-for="study-select" :invalid-feedback="$t('inputFieldFieldOfStudy') + ' ' + $t('is_required')">
        <b-form-select
          id="study-select"
          v-model="form.studySelection"
          required
          ref="studySelect"
          :state="studyState"
          :options="studyOptions"
          @change="onStudyChange"
        >
          <template #first>
            <b-form-select-option :value="null" disabled>{{ $t('placeholderFieldOfStudy') }}</b-form-select-option>
          </template>
        </b-form-select>
      </b-form-group>
      <b-form-group v-if="form.studySelection === 'Annet'" :label="$t('placeholderFieldOfStudy')" label-for="study-other-input" :invalid-feedback="$t('inputFieldFieldOfStudy') + ' ' + $t('is_required')">
        <b-form-input
          id="study-other-input"
          v-model="form.studyOther"
          required
          ref="studyOtherInput"
          :placeholder="$t('placeholderFieldOfStudy')"
          :state="studyOtherState"
        >
        </b-form-input>
      </b-form-group>
      <b-form-group :label="$t('inputFieldStudyYear')" label-for="year-input" :invalid-feedback="$t('inputFieldStudyYear') + ' ' + $t('is_required')">
        <b-form-select
          id="year-input"
          v-model="form.year"
          required
          ref="yearInput"
          :state="yearState"
          :options="yearOptions"
        >
          <template #first>
            <b-form-select-option :value="null" disabled>{{ $t('placeholderStudyYear') }}</b-form-select-option>
          </template>
        </b-form-select>
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
        studySelection: null,
        studyOther: '',
        year: null,
        allergies: ''
      },
      studyOptions: [
        { value: 'Bioteknologi', text: 'Bioteknologi' },
        { value: 'Bygg- og miljøteknikk', text: 'Bygg- og miljøteknikk' },
        { value: 'Datateknologi', text: 'Datateknologi' },
        { value: 'Elektronisk systemdesign og innovasjon', text: 'Elektronisk systemdesign og innovasjon' },
        { value: 'Energi og miljø', text: 'Energi og miljø' },
        { value: 'Geomatikk', text: 'Geomatikk' },
        { value: 'Industriell økonomi og teknologiledelse', text: 'Industriell økonomi og teknologiledelse' },
        { value: 'Kjemi og bioteknologi', text: 'Kjemi og bioteknologi' },
        { value: 'Kommunikasjonsteknologi', text: 'Kommunikasjonsteknologi' },
        { value: 'Kybernetikk og robotikk', text: 'Kybernetikk og robotikk' },
        { value: 'Marin teknikk', text: 'Marin teknikk' },
        { value: 'Maskinteknikk', text: 'Maskinteknikk' },
        { value: 'Materialteknologi', text: 'Materialteknologi' },
        { value: 'Nanoteknologi', text: 'Nanoteknologi' },
        { value: 'Produktutvikling og produksjon', text: 'Produktutvikling og produksjon' },
        { value: 'Teknisk fysikk', text: 'Teknisk fysikk' },
        { value: 'Annet', text: 'Annet' }
      ],
      yearOptions: [
        { value: '1', text: '1' },
        { value: '2', text: '2' },
        { value: '3', text: '3' },
        { value: '4', text: '4' },
        { value: '5', text: '5' }
      ],
      nameState: null,
      emailState: null,
      studyState: null,
      studyOtherState: null,
      yearState: null,
      allergiesState: null,
      emailInvalidFeedbackDefault: this.$t('inputFieldEmail') + ' ' + this.$t('is_required'),
      emailInvalidFeedbackString: this.emailInvalidFeedbackDefault
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
    }
  },
  methods: {
    checkFormValidity () {
      const nameValid = this.$refs.nameInput.checkValidity()
      const emailValid = this.$refs.emailInput.checkValidity()
      const studyValid = this.form.studySelection !== null
      const yearValid = this.form.year !== null
      const allergiesValid = true

      let studyOtherValid = true
      if (this.form.studySelection === 'Annet') {
        studyOtherValid = this.$refs.studyOtherInput && this.$refs.studyOtherInput.checkValidity()
        this.studyOtherState = studyOtherValid
      }

      this.nameState = nameValid
      this.emailState = emailValid
      this.studyState = studyValid
      this.yearState = yearValid
      this.allergiesState = allergiesValid

      return nameValid && emailValid && studyValid && yearValid && studyOtherValid
    },
    onStudyChange () {
      if (this.form.studySelection === 'Annet') {
        this.form.study = this.form.studyOther
      } else {
        this.form.study = this.form.studySelection
        this.form.studyOther = ''
      }
    },
    resetModal () {
      this.form.name = ''
      this.form.email = ''
      this.form.study = ''
      this.form.studySelection = null
      this.form.studyOther = ''
      this.form.year = null
      this.form.allergies = ''

      this.nameState = null
      this.emailState = null
      this.studyState = null
      this.studyOtherState = null
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

      // Set study field based on selection
      if (this.form.studySelection === 'Annet') {
        this.form.study = this.form.studyOther
      } else {
        this.form.study = this.form.studySelection
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
    }
  }
}
</script>
