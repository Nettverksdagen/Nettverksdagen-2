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
        <b-card header="Rediger Viktig informasjon" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-form-group label="Tittel" label-for="infobox-title-input">
              <b-form-input
                v-model="infobox.title"
                id="infobox-title-input"
                required
                placeholder="Skriv inn tittel"
              />
            </b-form-group>

            <b-form-group label="Tekst" label-for="infobox-paragraph-input">
              <b-form-textarea
                v-model="infobox.paragraph"
                id="infobox-paragraph-input"
                rows="5"
                required
                placeholder="Skriv inn informasjonstekst"
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
          <InfoBox :title="infobox.title" :paragraph="infobox.paragraph" />
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
        title: '',
        paragraph: ''
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
    title () {
      return this.$store.state.infobox.title || 'Viktig informasjon'
    },
    paragraph () {
      return this.$store.state.infobox.paragraph || ''
    }
  },
  created () {
    // Hent eksisterende infoboks fra store/API ved lasting
    this.$store.dispatch('infobox/fetchInfobox').then(() => {
      this.infobox.title = this.$store.state.infobox.title
      this.infobox.paragraph = this.$store.state.infobox.paragraph
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
