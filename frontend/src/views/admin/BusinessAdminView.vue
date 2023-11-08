<template>
  <div class="business-admin-view">
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
        <b-card header="Legg til en ny bedrift på forsiden" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group label="Firmanavn" label-for="business-name-input">
                  <b-form-input v-model="business.name" id="business-name-input" required placeholder="Skriv inn firmanavn" ></b-form-input>
                </b-form-group>
                <b-form-group label="Link til nettside (må starte med https://)" label-for="website-url-input">
                  <b-form-input type="url" v-model="business.website_url" id="website-url-input" required placeholder="Skriv inn link" @input="validateWebsiteUrl"></b-form-input>
                </b-form-group>
                <b-form-group label="Dager på stand" label-for="business-days-input">
                  <b-form-select v-model="business.days" :options="businessDays" id="business-days-input" required></b-form-select>
                </b-form-group>
                <b-form-group label="Standnummer" label-for="standnummer">
                  <b-form-input v-model="business.standnumber" id="standnummer" type="number" required></b-form-input>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Pakke" label-for="business-level-input">
                  <b-form-select v-model="business.level" :options="businessLevels" id="business-level-input" required></b-form-select>
                </b-form-group>
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" label="Logo" label-for="business-logo">
                    <b-form-file v-model="logoFile" :required="!editing" placeholder="Velg et bilde" id="business-logo" ref="logoFileInput" @input="uploadLogo"></b-form-file>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="logoSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-row>
              <div class="col-12">
                <b-form-group label="Tekst/info om bedrift (kan inneholde html)" label-for="business-name-input">
                  <b-form-textarea v-model="business.text" id="business-text-textarea" required placeholder="Tekst for å presentere bedriften :)" ></b-form-textarea>
                </b-form-group>
              </div>
              </b-row>
            <b-button type="submit" size="md" variant="success" v-if="!editing">{{$t('leggut')}}</b-button>
            <b-button type="submit" size="md" variant="primary" v-if="editing">{{$t('edit')}}</b-button>
            <b-button v-on:click="abortEdit()" size="md" variant="secondary" v-if="editing">{{$t('abort')}}</b-button>
          </b-form>
        </b-card>
      </div>
      <div class="d-none d-md-block col-4">
        <stand-map :isAdminPage=true style="width: 100%;"></stand-map>
        <!-- <b-jumbotron bg-variant="success" text-variant="white" :header="numBusinesses + ' bedrifter'" lead="lagt ut så langt." class="h-100">
        </b-jumbotron> -->
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Bedrifter">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="businesses">
            <template v-slot:cell(edit)="businesses">
              <edit-button class="mx-3" @click.native="edit(businesses.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(businesses.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="businesses">
            <template v-slot:cell(edit)="businesses">
              <edit-button class="mx-3" @click.native="edit(businesses.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(businesses.item)"></delete-button>
            </template>
          </b-table>
        </b-card>
      </div>
    </b-row>
  </div>
</template>
<script>
import axios from 'axios'
import ImagePreview from '@/components/admin/ImagePreview.vue'
import { mapMutations } from 'vuex'
import { fileUploader } from '@/services'
import EditButton from '@/components/admin/EditButton.vue'
import DeleteButton from '@/components/admin/DeleteButton.vue'
import StandMap from '../../components/anon/StandMap.vue'
export default {
  name: 'BusinessAdminView',
  components: {
    ImagePreview,
    EditButton,
    DeleteButton,
    StandMap
},
  data: function () {
    return {
      fields: [
        'id', { key: 'name', label: 'Name' }, { key: 'logo_uri', label: 'Logo Uri' },
        { key: 'website_url', label: 'Website Url' }, { key: 'level', label: 'Level' },
        { key: 'days', label: 'Days' },
        { key: 'textShort', label: 'Text' },
        { key: 'standnumber', label: 'Standnummer' },
        { key: 'edit', label: '' }
      ],
      business: {
        name: '',
        logo_uri: '',
        website_url: '',
        level: null,
        days: 'Ingen dager'
      },
      logoFile: null,
      showImgPreview: false,
      editing: false,
      alert: {
        dismissSecs: 5,
        dismissCountDown: 0,
        variant: 'info',
        heading: '',
        message: ''
      },
      businessLevels: [{value: null, text: 'Velg en pakke'}],
      businessDays: []
    }
  },
  computed: {
    businesses: function () {
      let b = this.$store.state.businesses.all
      for (let i = 0; i < b.length; i++) {
        if (b[i].text !== '') {
          b[i].textShort = b[i].text.substr(0, 30) + '...'
        } else {
          b[i].textShort = ''
        }
      }
      return b
    },
    numBusinesses: function () {
      return this.businesses.length
    },
    logoSrc: function () {
      return process.env.VUE_APP_FILESERVER_HOST + '/thumb/256/' + this.business.logo_uri
    }
  },
  beforeCreate: function () {
    axios.options(process.env.VUE_APP_API_HOST + '/api/business/').then((response) => {
      this.$data.businessLevels = this.$data.businessLevels.concat(response.data.actions.POST.level.choices.map(
        option => ({value: option.value, text: option.display_name})
      ))
    }).catch((e) => {
      this.showAlert('error',
        'Error ' + e.response.status + ' ' + e.response.statusText,
        'Kunne ikke lese skjema fra tjeneren. Prøv å laste siden på nytt.')
    })
    axios.options(process.env.VUE_APP_API_HOST + '/api/business/').then((response) => {
      this.$data.businessDays = this.$data.businessDays.concat(response.data.actions.POST.days.choices.map(
        option => ({value: option.value, text: option.display_name})
      ))
    }).catch((e) => {
      this.showAlert('error',
        'Error ' + e.response.status + ' ' + e.response.statusText,
        'Kunne ikke lese skjema fra tjeneren. Prøv å laste siden på nytt.')
    })
  },
  methods: {
    handleSubmit: function () {
      axios[(this.$data.editing ? 'put' : 'post')](process.env.VUE_APP_API_HOST + '/api/business/' +
            (this.$data.editing ? this.$data.business.id + '/' : ''), this.$data.business).then((response) => {
        this.showAlert('success', 'Suksess!', 'Bedriften er blitt ' +
           (this.$data.editing ? 'endret.' : 'lagt ut på forsiden.'))
        this['businesses/' + (this.$data.editing ? 'updateBusiness' : 'addBusiness')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Bedriften kunne ikke legges ut.')
      })
    },
    destroy: function (business) {
      if (!confirm('Er du sikker på at du vil slette ' + business.name + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/business/' +
        business.id + '/').then((response) => {
        this.showAlert('success', 'Suksess!', 'Bedriften er blitt slettet')
        this['businesses/deleteBusiness'](business)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Bedriften kunne ikke slettes.')
      })
      this.resetForm()
    },
    validateWebsiteUrl: function () {
      this.$data.business.website_url = this.validateLink(this.$data.business.website_url)
    },
    validateLink: function (link) {
      if (!(link.startsWith('https://') || link.startsWith('http://'))) {
        return 'https://'.concat(link)
      } else {
        return link
      }
    },
    resetForm: function () {
      this.$data.business = {name: '', logo_uri: '', website_url: '', level: null}
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
    countDownChanged: function (dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    },
    uploadLogo: function () {
      this.$data.showImgPreview = false
      this.$data.imgPreviewSrc = ''
      if (this.$data.logoFile === undefined || this.$data.logoFile === null) {
        return
      }
      fileUploader.uploadImage(this.$data.logoFile)
        .then((logoUri) => {
          this.$data.business.logo_uri = logoUri
          setTimeout(() => {
            this.$data.showImgPreview = true
          }, 30) // The image src can't be set at the same time as the img opacity or it will lose its transition
        })
        .catch((e) => {
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
    edit: function (business) {
      this.$data.business = business
      this.$data.showImgPreview = true
      this.$data.editing = true
    },
    abortEdit: function () {
      this.resetForm()
      this.$data.editing = false
    },
    ...mapMutations(['businesses/addBusiness', 'businesses/deleteBusiness', 'businesses/updateBusiness'])
  }
}
</script>

<style scoped lang="scss">

</style>
