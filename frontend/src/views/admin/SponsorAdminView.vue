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
        <b-card :header="$t('admin.sponsor.header')" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group :label="$t('admin.sponsor.sponsorName')" label-for="sponsor-name-input">
                  <b-form-input v-model="sponsor.name" id="sponsor-name-input" required :placeholder="$t('admin.sponsor.sponsorNamePlaceholder')" ></b-form-input>
                </b-form-group>
                <b-form-group :label="$t('admin.sponsor.websiteUrl')" label-for="website-url-input">
                  <b-form-input type="url" v-model="sponsor.website_url" id="website-url-input" required :placeholder="$t('admin.sponsor.websiteUrlPlaceholder')" @input="validateWebsiteUrl"></b-form-input>
                </b-form-group>
                <b-form-group :label="$t('admin.sponsor.sponsorType')" label-for="sponsor-type-input">
                  <b-form-select v-model="sponsor.type" id="sponsor-type-input" :options="sponsorTypes" required></b-form-select>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" :label="$t('admin.sponsor.logo')" label-for="sponsor-logo">
                    <b-form-file v-model="logoFile" :required="!editing" :placeholder="$t('admin.sponsor.selectImage')" id="sponsor-logo" ref="logoFileInput" @input="uploadLogo"></b-form-file>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="logoSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success" v-if="!editing">{{$t('leggut')}}</b-button>
            <b-button type="submit" size="md" variant="primary" v-if="editing">{{$t('admin.sponsor.updateSponsor')}}</b-button>
            <b-button v-on:click="abortEdit()" size="md" variant="secondary" v-if="editing">{{$t('abort')}}</b-button>
          </b-form>
        </b-card>
      </div>
      <div class="d-none d-md-block col-4">
        <b-jumbotron bg-variant="primary" text-variant="white" :header="numSponsors + ' ' + $t('admin.sponsor.sponsors')" :lead="$t('admin.sponsor.publishedSoFar')" class="h-100">
        </b-jumbotron>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card :header="$t('admin.sponsor.listHeader')">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="sponsors">
            <template v-slot:cell(edit)="sponsors">
              <edit-button class="mx-3" @click.native="edit(sponsors.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(sponsors.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="sponsors">
            <template v-slot:cell(edit)="sponsors">
              <edit-button class="mx-3" @click.native="edit(sponsors.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(sponsors.item)"></delete-button>
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
export default {
  name: 'SponsorAdminView',
  components: {
    ImagePreview,
    EditButton,
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        'id', { key: 'name', label: 'Name' }, { key: 'type', label: 'Type' }, { key: 'logo_uri', label: 'Logo Uri' },
        { key: 'website_url', label: 'Website Url' }, { key: 'edit', label: '' }
      ],
      sponsorTypes: [
        { value: 'Hovedsponsor', text: 'Hovedsponsor' },
        { value: 'Kaffesponsor', text: 'Kaffesponsor' },
        { value: 'Annen sponsor', text: 'Annen sponsor' }
      ],
      sponsor: {
        name: '',
        logo_uri: '',
        website_url: '',
        type: 'Annen sponsor'
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
      }
    }
  },
  computed: {
    sponsors: function () {
      return this.$store.state.sponsors.all
    },
    numSponsors: function () {
      return this.sponsors.length
    },
    logoSrc: function () {
      return process.env.VUE_APP_FILESERVER_HOST + '/thumb/256/' + this.sponsor.logo_uri
    }
  },
  methods: {
    handleSubmit: function () {
      axios[this.$data.editing ? 'put' : 'post'](process.env.VUE_APP_API_HOST + '/api/sponsor/' +
        (this.$data.editing ? this.$data.sponsor.id + '/' : ''), this.$data.sponsor).then((response) => {
        this.showAlert('success', this.$t('admin.success'), this.$t('admin.sponsor.listHeader') + ' ' +
            (this.$data.editing ? this.$t('admin.updated') : this.$t('admin.published')))
        this['sponsors/' + (this.$data.editing ? 'updateSponsor' : 'addSponsor')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          this.$t('admin.sponsor.listHeader') + ' ' + this.$t('admin.couldNotPublish'))
      })
    },
    destroy: function (sponsor) {
      if (!confirm(this.$t('admin.confirmDelete') + ' ' + sponsor.name + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/sponsor/' +
        sponsor.id + '/').then((response) => {
        this.showAlert('success', this.$t('admin.success'), this.$t('admin.sponsor.listHeader') + ' ' + this.$t('admin.deleted'))
        this['sponsors/deleteSponsor'](sponsor)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          this.$t('admin.sponsor.listHeader') + ' ' + this.$t('admin.couldNotDelete'))
      })
      this.resetForm()
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
      this.$data.sponsor = {name: '', logo_uri: '', website_url: '', type: 'Annen sponsor'}
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
          this.$data.sponsor.logo_uri = logoUri
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
            this.$t('admin.imageUploadFailed'))
          this.$data.showImgPreview = false
        })
    },
    edit: function (sponsor) {
      this.$data.sponsor = sponsor
      this.$data.showImgPreview = true
      this.$data.editing = true
    },
    abortEdit: function () {
      this.resetForm()
      this.$data.editing = false
    },
    ...mapMutations(['sponsors/addSponsor', 'sponsors/deleteSponsor', 'sponsors/updateSponsor'])
  }
}
</script>

<style scoped lang="scss">

</style>
