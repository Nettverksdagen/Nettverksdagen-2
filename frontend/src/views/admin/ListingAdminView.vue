<template>
  <div class="listing-admin-view">
    <b-alert :show="alert.dismissCountDown"
             dismissible
             fade
             :variant="alert.variant"
             @dismissed="alert.dismissCountDown=0"
             @dismiss-count-down="countDownChanged"
             class="mt-4">
      <h4 class="alert-heading font-weight-bold">{{ alert.heading }}</h4>
      <hr>
      {{ alert.message }}
    </b-alert>
    <b-row class="my-4">
      <div class="col-12 col-md-8">
        <b-card header="Legg ut en ny stillingsannonse" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group label="Stillingstittel" label-for="listing-name-input">
                  <b-form-input v-model="listing.name" id="listing-name-input" required placeholder="Velg en tittel" maxlength="100"></b-form-input>
                </b-form-group>
                <b-form-group label="Firmanavn" label-for="listing-company-input">
                  <b-form-input v-model="listing.company_name" id="listing-company-input" required placeholder="Skriv inn firmanavn" ></b-form-input>
                </b-form-group>
                <b-button type="submit" class="d-none d-md-block" size="md" variant="success">Opprett annonse</b-button>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Søknadsfrist" label-for="listing-deadline">
                  <datepicker v-model="deadlineDateTime" :typeable="true" :required="true" format="yyyy-MM-dd" placeholder="Trykk for å velge dato" :bootstrap-styling="true" :monday-first="true" id="listing-deadline"></datepicker>
                </b-form-group>
              </div>
            </b-row>
            <b-button type="submit" class="d-block d-md-none" size="md" variant="success">Opprett annonse</b-button>
          </b-form>
        </b-card>
      </div>
      <div class="d-none d-md-block col-4">
        <b-jumbotron bg-variant="info" text-variant="white" :header="numListings + ''" lead="åpne stillingsannonser" class="h-100">
        </b-jumbotron>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Stillingsannonser">
          <b-table hover :items="listings"></b-table>
        </b-card>
      </div>
    </b-row>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
import axios from 'axios'
export default {
  name: 'ListingAdminView',
  components: {
    Datepicker
  },
  data: function () {
    return {
      listing: {
        company_name: '',
        name: '',
        deadline: ''
      },
      deadlineDateTime: null,
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
    listings: function () {
      return this.$store.state.listings.all
    },
    numListings: function () {
      return this.listings.length
    }
  },
  methods: {
    handleSubmit: function () {
      this.$data.listing.deadline = this.$data.deadlineDateTime.toISOString().split('T')[0]
      axios.post('http://127.0.0.1:8000/api/listing/', this.$data.listing).then(() => {
        this.showAlert('success', 'Suksess!', 'Stillingsannonsen ble opprettet')
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Stillingsannonsen ble ikke opprettet')
      })
    },
    countDownChanged: function (dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    },
    showAlert: function (variant, heading, message) {
      this.alert.variant = variant
      this.alert.heading = heading
      this.alert.message = message
      this.alert.dismissCountDown = this.alert.dismissSecs
    }
  }
}
</script>

<style scoped>

</style>
