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
                <b-form-group label="Stillingstype" label-for="listing-company-type">
                  <b-form-select v-model="listing.type" :options="listingTypes" id="listing-company-type" required></b-form-select>
                </b-form-group>
                <b-form-group label="Sted" label-for="listing-city-input">
                  <b-form-input v-model="listing.city" id="listing-city-input" required placeholder="Skriv hvor jobben finner sted" maxlength="100"></b-form-input>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Søknadsfrist" label-for="listing-deadline">
                  <datepicker v-model="deadlineDateTime" :typeable="true" :required="true" format="yyyy-MM-dd" placeholder="Trykk for å velge dato" :bootstrap-styling="true" :monday-first="true" id="listing-deadline"></datepicker>
                </b-form-group>
                <b-form-group label="Link til annonse (må starte med https://)" label-for="listing-url-input">
                  <b-form-input type="url" v-model="listing.listing_url" id="listing-url-input" required placeholder="Skriv inn link" @input="validateLink"></b-form-input>
                </b-form-group>
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" label="Logo" label-for="listing-logo">
                    <b-form-file v-model="logoFile" required placeholder="Velg et bilde" ref="logoFileInput" @input="uploadLogo"></b-form-file>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="imgPreviewSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success">Opprett annonse</b-button>
          </b-form>
        </b-card>
      </div>
      <div class="d-none d-md-block col-4">
        <b-jumbotron bg-variant="info" text-variant="white" :header="numListings + ''" lead="åpne stillingsannonser" class="h-100">
          <hr class="my-4">
          <p>
            Her kan du legge inn nye stillingannonser og de vil dukke opp under
            <b-link :href="listingsLink.href" class="listings-link">{{ listingsLink.location.path }}</b-link>
          </p>
        </b-jumbotron>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Stillingsannonser">
          <b-table class="d-none d-md-table" hover :items="listings"></b-table>
          <b-table class="d-block d-md-none" stacked :items="listings"></b-table>
        </b-card>
      </div>
    </b-row>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
import axios from 'axios'
import { mapMutations } from 'vuex'
import ImagePreview from '@/components/admin/ImagePreview.vue'
import { fileUploader } from '@/services'
export default {
  name: 'ListingAdminView',
  components: {
    Datepicker,
    ImagePreview
  },
  data: function () {
    return {
      listing: {
        company_name: '',
        name: '',
        deadline: '',
        logo_uri: '',
        type: null,
        listing_url: '',
        city: ''
      },
      logoFile: null,
      showImgPreview: false,
      imgPreviewSrc: '',
      deadlineDateTime: null,
      alert: {
        dismissSecs: 5,
        dismissCountDown: 0,
        variant: 'info',
        heading: '',
        message: ''
      },
      listingTypes: [{value: null, text: 'Velg en stillingstype'}]
    }
  },
  computed: {
    listings: function () {
      return this.$store.state.listings.all
    },
    numListings: function () {
      return this.listings.length
    },
    listingsLink: function () {
      return this.$router.resolve({name: 'Listings'})
    }
  },
  methods: {
    handleSubmit: function () {
      this.$data.listing.deadline = this.$data.deadlineDateTime.toISOString().split('T')[0]
      axios.post(process.env.VUE_APP_API_HOST + '/api/listing/', this.$data.listing).then((response) => {
        this.showAlert('success', 'Suksess!', 'Stillingsannonsen ble opprettet.')
        this['listings/addListing'](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Stillingsannonsen ble ikke opprettet.')
      })
    },
    countDownChanged: function (dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    },
    resetForm: function () {
      this.$data.listing = {company_name: '', name: '', deadline: '', logo_uri: '', type: null, listing_url: '', city: ''}
      this.$data.deadlineDateTime = null
      this.$refs.logoFileInput.reset()
    },
    showAlert: function (variant, heading, message) {
      this.alert.variant = variant
      this.alert.heading = heading
      this.alert.message = message
      this.alert.dismissCountDown = this.alert.dismissSecs
    },
    uploadLogo: function () {
      this.$data.showImgPreview = false
      this.$data.imgPreviewSrc = ''
      if (this.$data.logoFile === undefined || this.$data.logoFile === null) {
        return
      }
      fileUploader.uploadImage(this.$data.logoFile)
        .then((logoUri) => {
          this.$data.imgPreviewSrc = process.env.VUE_APP_FILESERVER_HOST + '/' + logoUri
          this.$data.listing.logo_uri = logoUri
          setTimeout(() => {
            this.$data.showImgPreview = true
          }, 30) // The image src can't be set at the same time as the img opacity or it will lose its transition
        }).catch((e) => {
          let errorTitle = 'Error'
          if (e.response !== undefined) {
            errorTitle = 'Error ' + e.response.status + ' ' + e.response.statusText
          }
          this.showAlert('danger',
            errorTitle,
            'Bildeopplastning feilet, prøv igjen. Kontakt IT om problemet vedvarer.')
          this.$data.showImgPreview = false
          this.$data.imgPreviewSrc = ''
        })
    },
    validateLink: function () {
      if (!(this.$data.listing.listing_url.startsWith('https://') || this.$data.listing.listing_url.startsWith('http://'))) {
        this.$data.listing.listing_url = 'https://'.concat(this.$data.listing.listing_url)
      }
    },
    ...mapMutations(['listings/addListing'])
  },
  beforeCreate: function () {
    axios.options(process.env.VUE_APP_API_HOST + '/api/listing/').then((response) => {
      this.$data.listingTypes = this.$data.listingTypes.concat(response.data.actions.POST.type.choices.map(
        option => ({value: option.value, text: option.display_name})
      ))
    }).catch((e) => {
      this.showAlert('error',
        'Error ' + e.response.status + ' ' + e.response.statusText,
        'Kunne ikke lese skjema fra tjeneren. Prøv å laste siden på nytt.')
    })
  }
}
</script>

<style scoped lang="scss">
.listings-link {
  color:#fff;
}
</style>
