<template>
  <div class="listing-admin-view">
    <b-row class="my-4">
      <div class="col-12 col-md-8">
        <b-card header="Legg ut en ny stillingsannonse" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group label="Stillingstittel" label-for="listing-name-input">
                  <b-form-input v-model="name" id="listing-name-input" required placeholder="Velg en tittel" maxlength="100"></b-form-input>
                </b-form-group>
                <b-form-group label="Firmanavn" label-for="listing-company-input">
                  <b-form-input v-model="company_name" id="listing-company-input" required placeholder="Skriv inn firmanavn" ></b-form-input>
                </b-form-group>
                <b-button type="submit" class="d-none d-md-block" size="md" variant="success">Opprett annonse</b-button>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Søknadsfrist" label-for="listing-deadline">
                  <datepicker v-model="deadline" :typeable="true" :required="true" format="yyyy-MM-dd" placeholder="Trykk for å velge dato" :bootstrap-styling="true" :monday-first="true" id="listing-deadline"></datepicker>
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
      company_name: '',
      name: '',
      deadline: null
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
      this.$data.deadline = this.$data.deadline.toISOString().split('T')[0]
      axios.post('http://127.0.0.1:8000/api/listing/', this.$data).then(() => {
        console.log('Successfully created new listing') // TODO: Implement success callback
      }).catch(() => {
        console.log('Failed to create listing') // TODO: Implement fail callback
      })
    }
  }
}
</script>

<style scoped>

</style>
