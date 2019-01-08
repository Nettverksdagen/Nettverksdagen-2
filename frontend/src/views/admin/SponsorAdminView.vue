<template>
  <div class="sponsor-admin-view">
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
        <b-card header="Legg til en ny sponsor på forsiden" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group label="Sponsornavn" label-for="sponsor-name-input">
                  <b-form-input v-model="sponsor.name" id="sponsor-name-input" required placeholder="Skriv inn sponsornavn" ></b-form-input>
                </b-form-group>
                <b-form-group label="Link til nettside (må starte med https://)" label-for="website-url-input">
                  <b-form-input type="url" v-model="sponsor.website_url" id="website-url-input" required placeholder="Skriv inn link" @input="validateWebsiteUrl"></b-form-input>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" label="Logo" label-for="sponsor-logo">
                    <b-form-file v-model="logoFile" required placeholder="Velg et bilde" id="sponsor-logo" ref="logoFileInput" @input="uploadLogo"></b-form-file>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="imgPreviewSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success">Legg ut sponsoren</b-button>
          </b-form>
        </b-card>
      </div>
      <div class="d-none d-md-block col-4">
        <b-jumbotron bg-variant="primary" text-variant="white" :header="numSponsors + ' sponsorer'" lead="lagt ut så langt." class="h-100">
        </b-jumbotron>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Sponsorer">
          <b-table class="d-none d-md-table" hover :items="sponsors"></b-table>
          <b-table class="d-block d-md-none" stacked :items="sponsors"></b-table>
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
  name: 'SponsorAdminView',
  components: {
    ImagePreview
  },
  data: function () {
    return {
      sponsor: {
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
    sponsors: function () {
      return this.$store.state.sponsors.all
    },
    numSponsors: function () {
      return this.sponsors.length
    }
  },
  methods: {
    handleSubmit: function () {
      axios.post(process.env.VUE_APP_API_HOST + '/api/sponsor/', this.$data.sponsor).then((response) => {
        this.showAlert('success', 'Suksess!', 'Sponsoren er blitt lagt ut på forsiden.')
        this['sponsors/addSponsor'](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Sponsoren kunne ikke legges ut.')
      })
    },
    validateWebsiteUrl: function () {
      this.$data.sponsor.website_url = this.validateLink(this.$data.sponsor.website_url)
    },
    validateLink: function (link) {
      if (!(link.startsWith('https://') || link.startsWith('http://'))) {
        return 'https://'.concat(link)
      } else {
        return link
      }
    },
    resetForm: function () {
      this.$data.sponsor = {name: '', logo_uri: '', website_url: ''}
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
          this.$data.sponsor.logo_uri = logoUri
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
    ...mapMutations(['sponsors/addSponsor'])
  }
}
</script>

<style scoped lang="scss">

</style>
