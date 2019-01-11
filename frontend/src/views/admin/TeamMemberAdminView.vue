<template>
  <div class="team-member-admin-view">
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
      <div class="col-12">
        <b-card header="Legg ut et styremedlem på kontaktsiden" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group label="Fullt navn" label-for="member-name-input">
                  <b-form-input v-model="teamMember.name" id="member-name-input" required placeholder="Skriv inn fullt navn" ></b-form-input>
                </b-form-group>
                <b-form-group label="Mailadresse" label-for="member-email-input">
                  <b-form-input type="email" v-model="teamMember.email" id="member-email-input" required placeholder="Skriv inn mailadresse"></b-form-input>
                </b-form-group>
                <b-form-group label="Team" label-for="member-team-input">
                  <b-form-input v-model="teamMember.team" id="member-team-input" required placeholder="F.eks Styret"></b-form-input>
                  <p class="text-black-50 mt-2">
                    <span class="font-weight-bold">Merk</span>:
                    Medlemmer grupperes på kontaktsiden etter hvilket team de hører hjemme i.
                    Pass på at alle i samme team skrives opp med nøyaktig samme teamnavn, ellers vil de havne i forskjellige kategorier.
                    Det er lurt å dobbeltsjekke på kontaktsiden om alt stemmer etter du har lagt inn et medlem
                  </p>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Stilling" label-for="member-position-input">
                  <b-form-input v-model="teamMember.position" id="member-position-input" required placeholder="Skriv inn stilling"></b-form-input>
                </b-form-group>
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" label="Bilde" label-for="member-photo">
                    <b-form-file v-model="photoFile" required placeholder="Velg et bilde" id="member-photo" ref="photoFileInput" @input="uploadPhoto"></b-form-file>
                    <p class="text-black-50 mt-2">
                      <span class="font-weight-bold">Obs</span>:
                      Bildet blir automatisk plassert i sentrum av et kvadrat, men ikke beskåret eller strukket.
                      Last opp bilder som allerede er kvadratiske for best effekt.
                    </p>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="imgPreviewSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success">Legg ut medlemmet</b-button>
          </b-form>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Teammedlemmer">
          <b-table class="d-none d-md-table" hover :items="teamMembers"></b-table>
          <b-table class="d-block d-md-none" stacked :items="teamMembers"></b-table>
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
  name: 'TeamMemberAdminView',
  components: {
    ImagePreview
  },
  data: function () {
    return {
      teamMember: {
        name: '',
        email: '',
        team: '',
        position: '',
        photo_uri: ''
      },
      photoFile: null,
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
    teamMembers: function () {
      return this.$store.state.teamMembers.all
    }
  },
  methods: {
    handleSubmit: function () {
      axios.post(process.env.VUE_APP_API_HOST + '/api/teammember/', this.$data.teamMember).then((response) => {
        this.showAlert('success', 'Suksess!', 'Teammedlemmet er blitt lagt ut på forsiden.')
        this['teamMembers/addTeamMember'](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Teammedlemmet kunne ikke legges ut.')
      })
    },
    resetForm: function () {
      this.$data.teamMember = {name: '', email: '', team: '', position: '', photo_uri: ''}
      this.$refs.photoFileInput.reset()
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
    uploadPhoto: function () {
      this.$data.showImgPreview = false
      this.$data.imgPreviewSrc = ''
      if (this.$data.photoFile === undefined || this.$data.photoFile === null) {
        return
      }
      fileUploader.uploadImage(this.$data.photoFile)
        .then((photoUri) => {
          this.$data.teamMember.photo_uri = photoUri
          this.$data.imgPreviewSrc = process.env.VUE_APP_FILESERVER_HOST + '/' + photoUri
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
    ...mapMutations(['teamMembers/addTeamMember'])
  }
}
</script>

<style lang="scss" scoped>

</style>
