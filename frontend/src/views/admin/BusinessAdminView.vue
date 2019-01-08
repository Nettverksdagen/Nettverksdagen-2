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
              </div>
              <div class="col-12 col-md-6">
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" label="Logo" label-for="business-logo">
                    <b-form-file v-model="logoFile" required placeholder="Velg et bilde" id="business-logo" ref="logoFileInput" @input="uploadLogo"></b-form-file>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="imgPreviewSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success">Legg ut bedriften</b-button>
          </b-form>
        </b-card>
      </div>
      <div class="d-none d-md-block col-4">
        <b-jumbotron bg-variant="success" text-variant="white" :header="numBusinesses + ' bedrifter'" lead="lagt ut så langt." class="h-100">
        </b-jumbotron>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Bedrifter">
          <b-table class="d-none d-md-table" hover :items="businesses"></b-table>
          <b-table class="d-block d-md-none" stacked :items="businesses"></b-table>
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
export default {
  name: 'BusinessAdminView',
  components: {
    ImagePreview
  },
  data: function () {
    return {
      business: {
        name: '',
        logo_uri: '',
        website_url: ''
      },
      logoFile: null,
      showImgPreview: false,
      imgPreviewSrc: '',
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
    businesses: function () {
      return this.$store.state.businesses.all
    },
    numBusinesses: function () {
      return this.businesses.length
    }
  },
  methods: {
    handleSubmit: function () {
      axios.post(process.env.VUE_APP_API_HOST + '/api/business/', this.$data.business).then((response) => {
        this.showAlert('success', 'Suksess!', 'Bedriften er blitt lagt ut på forsiden.')
        this['businesses/addBusiness'](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Bedriften kunne ikke legges ut.')
      })
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
      this.$data.business = {name: '', logo_uri: '', website_url: ''}
      this.$refs.logoFileInput.reset()
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
          this.$data.imgPreviewSrc = process.env.VUE_APP_FILESERVER_HOST + '/' + logoUri
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
          this.$data.imgPreviewSrc = ''
        })
    },
    ...mapMutations(['businesses/addBusiness'])
  }
}
</script>

<style scoped lang="scss">

</style>
