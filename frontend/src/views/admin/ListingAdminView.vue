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
                  <p class="text-black-50 mt-2">
                    <span class="font-weight-bold">Merk</span>:
                    For å opprette stillingsannonser for flere enn én jobblokasjon, skriv en liste med kommaseparerte steder.
                    F.eks: "Oslo, Bergen, Trondheim".
                  </p>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Søknadsfrist (la stå blank for løpende frist)" label-for="listing-deadline">
                  <datepicker v-model="deadlineDateTime" :typeable="true" :required="false" format="yyyy-MM-dd" placeholder="Trykk for å velge dato" :bootstrap-styling="true" :monday-first="true" id="listing-deadline"></datepicker>
                </b-form-group>
                <b-form-group label="Link til annonse (må starte med https://)" label-for="listing-url-input">
                  <b-form-input type="url" v-model="listing.listing_url" id="listing-url-input" required placeholder="Skriv inn link" @input="validateLink"></b-form-input>
                </b-form-group>
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" label="Logo" label-for="listing-logo">
                    <b-form-file v-model="logoFile" :required="!editing" placeholder="Velg et bilde" ref="logoFileInput" @input="uploadLogo"></b-form-file>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="imgSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-row>
              <div class="col-12">
                <b-form-group label="Intern link til annonse" label-for="internal-url-input">
                  <b-form-input v-model="listing.internal_url" id="internal-url-input" placeholder="Skriv inn intern link"></b-form-input>
                  <p class="text-black-50 mt-2">
                    <span class="font-weight-bold">{{$t('merk')}}</span>:
                    {{$t('lastpart')}}
                  </p>
                </b-form-group>
                <b-form-group label="Innhold i intern stillingsannonse (kan inneholde html)" label-for="content-input">
                  <b-form-textarea v-model="listing.content" id="content-textarea" placeholder="Eventuelt innhold i stillingsannonsen" ></b-form-textarea>
                </b-form-group>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success" v-if="!editing">Opprett annonse</b-button>
            <b-button type="submit" size="md" variant="primary" v-if="editing">Endre annonse</b-button>
            <b-button v-on:click="abortEdit()" size="md" variant="secondary" v-if="editing">Avbryt</b-button>
          </b-form>
        </b-card>
      </div>
      <div class="d-none d-md-block col-4">
        <b-jumbotron bg-variant="info" text-variant="white" :header="numListings + ''" lead="åpne stillingsannonser" class="h-100">
          <hr class="my-4">
          <p>
            {{$t('herestilling')}}
            <b-link :href="listingsLink.href" class="listings-link">{{ listingsLink.location.path }}</b-link>
          </p>
        </b-jumbotron>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Stillingsannonser">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="listings">
            <template v-slot:cell(edit)="listings">
              <edit-button class="mx-3" @click.native="edit(listings.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(listings.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="listings">
            <template v-slot:cell(edit)="listings">
              <edit-button class="mx-3" @click.native="edit(listings.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(listings.item)"></delete-button>
            </template>
          </b-table>
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
import EditButton from '@/components/admin/EditButton.vue'
import DeleteButton from '@/components/admin/DeleteButton.vue'
export default {
  name: 'ListingAdminView',
  components: {
    Datepicker,
    ImagePreview,
    EditButton,
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        'id', { key: 'name', label: 'Name' }, { key: 'company_name', label: 'Company Name' },
        { key: 'deadline', label: 'deadline' }, { key: 'logo_uri', label: 'Logo Uri' },
        { key: 'type', label: 'Type' }, { key: 'listing_url', label: 'Listing Url' },
        { key: 'city', label: 'City' }, { key: 'internal_url', label: 'Internal Url' },
        { key: 'contentShort', label: 'Content' }, { key: 'edit', label: '' }
      ],
      listing: {
        company_name: '',
        name: '',
        deadline: '',
        logo_uri: '',
        type: null,
        listing_url: '',
        city: '',
        internal_url: '',
        content: ''
      },
      logoFile: null,
      showImgPreview: false,
      deadlineDateTime: null,
      editing: false,
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
      let l = this.$store.state.listings.all
      for (let i = 0; i < l.length; i++) {
        if (l[i].content !== '') {
          l[i].contentShort = l[i].content.substr(0, 30) + '...'
        } else {
          l[i].contentShort = ''
        }
      }
      return l
    },
    numListings: function () {
      return this.listings.length
    },
    listingsLink: function () {
      return this.$router.resolve({name: 'Listings'})
    },
    imgSrc: function () {
      return process.env.VUE_APP_FILESERVER_HOST + '/thumb/256/' + this.listing.logo_uri
    }
  },
  methods: {
    handleSubmit: function () {
      if (this.$data.deadlineDateTime !== null) {
        this.$data.listing.deadline = this.$data.deadlineDateTime.toISOString().split('T')[0]
      } else {
        this.$data.listing.deadline = null
      }
      axios[this.$data.editing ? 'put' : 'post'](process.env.VUE_APP_API_HOST + '/api/listing/' +
        (this.$data.editing ? this.$data.listing.id + '/' : ''), this.$data.listing).then((response) => {
        this.showAlert('success', 'Suksess!', 'Stillingsannonsen ble ' + (this.$data.editing ? 'endret.' : 'opprettet.'))
        this['listings/' + (this.$data.editing ? 'updateListing' : 'addListing')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Stillingsannonsen ble ikke opprettet.')
      })
    },
    destroy: function (listing) {
      if (!confirm('Er du sikker på at du vil slette ' + listing.name + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/listing/' +
        listing.id + '/').then((response) => {
        this.showAlert('success', 'Suksess!', 'Annonsen ble slettet')
        this['listings/deleteListing'](listing)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Stillingsannonsen kunne ikke slettes.')
      })
      this.resetForm()
    },
    countDownChanged: function (dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    },
    resetForm: function () {
      this.$data.listing = {company_name: '', name: '', deadline: '', logo_uri: '', type: null, listing_url: '', city: ''}
      this.$data.deadlineDateTime = null
      this.$refs.logoFileInput.reset()
      this.$data.editing = false
      this.$data.showImgPreview = false
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
        })
    },
    validateLink: function () {
      if (!(this.$data.listing.listing_url.startsWith('https://') || this.$data.listing.listing_url.startsWith('http://'))) {
        this.$data.listing.listing_url = 'https://'.concat(this.$data.listing.listing_url)
      }
    },
    edit: function (listing) {
      this.$data.listing = listing
      this.$data.showImgPreview = true
      this.$data.editing = true
      this.$data.deadlineDateTime = new Date(this.$data.listing.deadline)
    },
    abortEdit: function () {
      this.resetForm()
      this.$data.editing = false
    },
    ...mapMutations(['listings/addListing', 'listings/deleteListing', 'listings/updateListing'])
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
.d-md-table {
  table-layout: fixed;
}
</style>
