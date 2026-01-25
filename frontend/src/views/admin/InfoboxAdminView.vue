<template>
  <div class="infobox-admin-view">
    <b-alert
      :show="alert.dismissCountDown"
      dismissible
      fade
      :variant="alert.variant"
      @dismissed="alert.dismissCountDown = 0"
      @dismiss-count-down="countDownChanged"
      class="mt-4"
    >
      <h4 class="alert-heading font-weight-bold">{{ alert.heading }}</h4>
      <hr />
      {{ alert.message }}
    </b-alert>

    <b-row class="my-4">
      <div class="col-12 col-md-8">
        <b-card header="Rediger infoboksen på forsiden" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <h5 class="mt-3 mb-3">Norsk</h5>
            <b-form-group label="Tittel" label-for="infobox-title-nb-input">
              <b-form-input
                v-model="infobox.title_nb"
                id="infobox-title-nb-input"
                placeholder="Skriv inn tittel"
              />
            </b-form-group>

            <b-form-group label="Tekst" label-for="infobox-paragraph-nb-input">
              <b-form-textarea
                v-model="infobox.paragraph_nb"
                id="infobox-paragraph-nb-input"
                rows="5"
                placeholder="Skriv inn informasjonstekst"
              />
            </b-form-group>

            <hr>

            <h5 class="mt-3 mb-3">English</h5>
            <b-form-group label="Title" label-for="infobox-title-en-input">
              <b-form-input
                v-model="infobox.title_en"
                id="infobox-title-en-input"
                placeholder="Write title"
              />
            </b-form-group>

            <b-form-group label="Text" label-for="infobox-paragraph-en-input">
              <b-form-textarea
                v-model="infobox.paragraph_en"
                id="infobox-paragraph-en-input"
                rows="5"
                placeholder="Write information text"
              />
            </b-form-group>

            <b-button type="submit" size="md" variant="success">
              Lagre endringer
            </b-button>
          </b-form>
        </b-card>
      </div>
    </b-row>

    <b-row>
      <div class="col-12">
        <b-card header="Forhåndsvisning">
          <h5 class="mt-3 mb-3">Norsk</h5>
          <InfoBox :title="infobox.title_nb" :paragraph="infobox.paragraph_nb" />
          <hr class="mt-4">
          <h5 class="mt-3 mb-3">English</h5>
          <InfoBox :title="infobox.title_en" :paragraph="infobox.paragraph_en" />
        </b-card>
      </div>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios'
import InfoBox from '@/components/anon/InfoBox.vue'

export default {
  name: 'InfoBoxAdminView',
  components: { InfoBox },
  data () {
    return {
      infobox: {
        title_nb: '',
        title_en: '',
        paragraph_nb: '',
        paragraph_en: ''
      },
      alert: {
        dismissSecs: 5,
        dismissCountDown: 0,
        variant: 'info',
        heading: '',
        message: ''
      }
    }
  },
  computed: {
    title_nb () {
      return this.$store.state.infobox.title_nb || ''
    },
    title_en () {
      return this.$store.state.infobox.title_en || ''
    },
    paragraph_nb () {
      return this.$store.state.infobox.paragraph_nb || ''
    },
    paragraph_en () {
      return this.$store.state.infobox.paragraph_en || ''
    }
  },
  created () {
    // Hent eksisterende infoboks fra store/API ved lasting
    this.$store.dispatch('infobox/fetchInfobox').then(() => {
      this.infobox = {
          title_nb: this.$store.state.infobox.title_nb || '',
          title_en: this.$store.state.infobox.title_en || '',
          paragraph_nb: this.$store.state.infobox.paragraph_nb || '',
          paragraph_en: this.$store.state.infobox.paragraph_en || ''
      }
    })
  },
  methods: {
    handleSubmit () {
      axios
        .post(process.env.VUE_APP_API_HOST + '/api/infobox/', this.infobox)
        .then(() => {
          this.showAlert('success', 'Suksess!', 'Infoboksen er oppdatert.')
          this.$store.commit('infobox/fetchSuccessful', this.infobox)
        })
        .catch((e) => {
          const status = e.response ? e.response.status : ''
          const text = e.response ? e.response.statusText : ''
          this.showAlert(
            'danger',
            `Error ${status} ${text}`,
            'Kunne ikke lagre infoboksen.'
          )
        })
    },
    showAlert (variant, heading, message) {
      this.alert.variant = variant
      this.alert.heading = heading
      this.alert.message = message
      this.alert.dismissCountDown = this.alert.dismissSecs
    },
    countDownChanged (dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    }
  }
}
</script>

<style scoped lang="scss">
</style>
