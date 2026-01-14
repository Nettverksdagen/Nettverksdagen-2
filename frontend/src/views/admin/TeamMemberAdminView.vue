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
        <b-card :header="$t('admin.teamMember.header')" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group :label="$t('teamMember.fullName')" label-for="member-name-input">
                  <b-form-input v-model="teamMember.name" id="member-name-input" required :placeholder="$t('teamMember.placeholder.name')"></b-form-input>
                </b-form-group>
                <b-form-group :label="$t('teamMember.emailLabel')" label-for="member-email-input">
                  <b-form-input type="email" v-model="teamMember.email" id="member-email-input" required :placeholder="$t('teamMember.placeholder.email')"></b-form-input>
                </b-form-group>
                <b-form-group :label="$t('teamMember.teamLabel')" label-for="member-team-input">
                  <b-form-input v-model="teamMember.team" id="member-team-input" required :placeholder="$t('teamMember.placeholder.team')"></b-form-input>
                  <p class="text-black-50 mt-2">
                    <span class="font-weight-bold">{{$t('merk')}}</span>:
                    {{$t('medlemgruppe')}}
                  </p>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group :label="$t('teamMember.positionLabel')" label-for="member-position-input">
                  <b-form-input v-model="teamMember.position" id="member-position-input" required :placeholder="$t('teamMember.placeholder.position')"></b-form-input>
                </b-form-group>
                <div class="d-flex">
                  <b-form-group class="flex-grow-1" :label="$t('teamMember.photoLabel')" label-for="member-photo">
                    <b-form-file v-model="photoFile" :placeholder="$t('teamMember.placeholder.photo')" id="member-photo" ref="photoFileInput" @input="uploadPhoto"></b-form-file>
                    <p class="text-black-50 mt-2">
                      <span class="font-weight-bold">{{$t('nbLabel')}}</span>:
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
        <b-card :header="$t('admin.teamMember.listHeader')">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="teamMembers">
            <template v-slot:cell(edit)="row">
              <edit-button class="mx-3" @click.native="edit(row.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(row.item)"></delete-button>
            </template>
            <template v-slot:cell(position)="row">
              {{ translatePosition(row.item.position) }}
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="teamMembers">
            <template v-slot:cell(edit)="row">
              <edit-button class="mx-3" @click.native="edit(row.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(row.item)"></delete-button>
            </template>
            <template v-slot:cell(position)="row">
              {{ translatePosition(row.item.position) }}
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
    // translated table column labels
    fields: function () {
      return [
        'id',
        { key: 'name', label: this.$t('teamMember.column.name') },
        { key: 'email', label: this.$t('teamMember.column.email') },
        { key: 'photo_uri', label: this.$t('teamMember.column.photo') },
        { key: 'team', label: this.$t('teamMember.column.team') },
        { key: 'position', label: this.$t('teamMember.column.position') },
        { key: 'edit', label: '' }
      ]
    },
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
    translatePosition: function (pos) {
      if (!pos) return ''
      const map = {
        'Markedsføringsansvarlig': this.$t('teamMember.positions.Markedsføringsansvarlig'),
        'Sekretær': this.$t('teamMember.positions.Sekretær'),
        'Leder': this.$t('teamMember.positions.Leder'),
        'Nestleder': this.$t('teamMember.positions.Nestleder'),
        'Sponsoransvarlig': this.$t('teamMember.positions.Sponsoransvarlig'),
        'IT-ansvarlig': this.$t('teamMember.positions.IT-ansvarlig'),
        'Bedriftansvarlig': this.$t('teamMember.positions.Bedriftansvarlig'),
        'Medlem': this.$t('teamMember.positions.Medlem')
      }
      return map[pos] || pos
    },
    handleSubmit: function () {
      axios[(this.$data.editing ? 'put' : 'post')](process.env.VUE_APP_API_HOST +
        '/api/teammember/' + (this.$data.editing ? this.$data.teamMember.id + '/' : ''),
      this.$data.teamMember).then((response) => {
        this.showAlert('success',
          this.$t('success'),
          this.$t(this.$data.editing ? 'teamMember.successUpdated' : 'teamMember.successCreated', {name: response.data.name}))
        this['teamMembers/' + (this.$data.editing ? 'updateTeamMember' : 'addTeamMember')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          this.$t('error') + (e.response ? ' ' + e.response.status + ' ' + e.response.statusText : ''),
          this.$t('teamMember.createError'))
      })
    },
    destroy: function (teamMember) {
      if (!confirm(this.$t('teamMember.deleteConfirm', {name: teamMember.name}))) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/teammember/' +
        teamMember.id + '/').then((response) => {
        this.showAlert('success', this.$t('success'), this.$t('teamMember.deleteSuccess', {name: teamMember.name}))
        this['teamMembers/deleteTeamMember'](teamMember)
      }).catch((e) => {
        this.showAlert('danger',
          this.$t('error') + (e.response ? ' ' + e.response.status + ' ' + e.response.statusText : ''),
          this.$t('teamMember.deleteError'))
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
          }, 30)
        })
        .catch((e) => {
          let errorTitle = this.$t('error')
          if (e.response !== undefined) {
            errorTitle = this.$t('error') + ' ' + e.response.status + ' ' + e.response.statusText
          }
          this.showAlert('danger',
            errorTitle,
            this.$t('teamMember.uploadError'))
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
