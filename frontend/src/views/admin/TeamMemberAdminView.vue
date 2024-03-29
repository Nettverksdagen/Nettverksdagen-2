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
                    <span class="font-weight-bold">{{$t('merk')}}</span>:
                    {{$t('medlemgruppe')}}
                  </p>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Stilling" label-for="member-position-input">
                  <b-form-input v-model="teamMember.position" id="member-position-input" required placeholder="Skriv inn stilling"></b-form-input>
                </b-form-group>
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" label="Bilde" label-for="member-photo">
                    <b-form-file v-model="photoFile" placeholder="Velg et bilde" id="member-photo" ref="photoFileInput" @input="uploadPhoto"></b-form-file>
                    <p class="text-black-50 mt-2">
                      <span class="font-weight-bold">NB!</span>:
                      {{$t('squarephoto')}}
                    </p>
                  </b-form-group>
                  <image-preview :imgPreviewSrc="imgSrc" :showImgPreview="showImgPreview"></image-preview>
                </div>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success" v-if="!editing">{{$t('leggut')}}</b-button>
            <b-button type="submit" size="md" variant="primary" v-if="editing">{{$t('edit')}}</b-button>
            <b-button v-on:click="abortEdit()" size="md" variant="secondary" v-if="editing">{{$t('abort')}}</b-button>
          </b-form>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Teammedlemmer">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="teamMembers">
            <template v-slot:cell(edit)="teamMembers">
              <edit-button class="mx-3" @click.native="edit(teamMembers.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(teamMembers.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="teamMembers">
            <template v-slot:cell(edit)="teamMembers">
              <edit-button class="mx-3" @click.native="edit(teamMembers.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(teamMembers.item)"></delete-button>
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
  name: 'TeamMemberAdminView',
  components: {
    ImagePreview,
    EditButton,
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        'id', { key: 'name', label: 'Name' }, { key: 'email', label: 'Email' },
        { key: 'photo_uri', label: 'Photo Uri' }, { key: 'team', label: 'Team' },
        { key: 'position', label: 'Position' }, { key: 'edit', label: '' }
      ],
      teamMember: {
        name: '',
        email: '',
        team: '',
        position: '',
        photo_uri: ''
      },
      photoFile: null,
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
    teamMembers: function () {
      return this.$store.state.teamMembers.all
    },
    imgSrc: function () {
      if (this.teamMember.photo_uri) {
        return process.env.VUE_APP_FILESERVER_HOST + '/thumb/256/' + this.teamMember.photo_uri
      } else {
        return 'https://d2ojdbp0769afo.cloudfront.net/fnd/v4/static/images/BlankProfile.png'
      }
    }
  },
  methods: {
    handleSubmit: function () {
      axios[(this.$data.editing ? 'put' : 'post')](process.env.VUE_APP_API_HOST +
        '/api/teammember/' + (this.$data.editing ? this.$data.teamMember.id + '/' : ''),
      this.$data.teamMember).then((response) => {
        this.showAlert('success', 'Suksess!', 'Teammedlemmet er blitt ' +
          (this.$data.editing ? 'endret.' : 'lagt ut på forsiden.'))
        this['teamMembers/' + (this.$data.editing ? 'updateTeamMember' : 'addTeamMember')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Teammedlemmet kunne ikke legges ut.')
      })
    },
    destroy: function (teamMember) {
      if (!confirm('Er du sikker på at du vil slette ' + teamMember.name + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/teammember/' +
        teamMember.id + '/').then((response) => {
        this.showAlert('success', 'Suksess!', 'Teammedlemmet er blitt slettet')
        this['teamMembers/deleteTeamMember'](teamMember)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Teammedlemmet kunne ikke slettes.')
      })
      this.resetForm()
    },
    resetForm: function () {
      this.$data.teamMember = {name: '', email: '', team: '', position: '', photo_uri: ''}
      this.$refs.photoFileInput.reset()
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
    uploadPhoto: function () {
      this.$data.showImgPreview = false
      this.$data.imgPreviewSrc = ''
      if (this.$data.photoFile === undefined || this.$data.photoFile === null) {
        return
      }
      fileUploader.uploadImage(this.$data.photoFile)
        .then((photoUri) => {
          this.$data.teamMember.photo_uri = photoUri
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
            'Bildeopplastning feilet, prøv igjen. Kontakt IT om problemet vedvarer. IT: Prøv å restart serveren.')
          this.$data.showImgPreview = false
        })
    },
    edit: function (teamMember) {
      this.$data.teamMember = teamMember
      this.$data.showImgPreview = true
      this.$data.editing = true
    },
    abortEdit: function () {
      this.resetForm()
      this.$data.editing = false
    },
    ...mapMutations(['teamMembers/addTeamMember', 'teamMembers/deleteTeamMember',
      'teamMembers/updateTeamMember'])
  }
}
</script>

<style lang="scss" scoped>

</style>
