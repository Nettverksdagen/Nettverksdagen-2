<template>
  <div class="form-admin-view">
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
        <b-card header="Legg til nytt Google-skjema" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group label="Google Forms-url" label-for="form-external-url-input">
                  <b-form-input v-model="form.external_url" id="form-external-url-input" required placeholder="https://docs.google.com/forms..." ></b-form-input>
                </b-form-group>
                <b-form-group label="Intern Nettverksdagene.no-url (kun den delen som kommer etter nettverksdagene.no/skjema/)" label-for="form-internal-url-input">
                  <b-form-input v-model="form.internal_url" id="form-internal-url-input" required placeholder="Intern skjema-url" ></b-form-input>
                </b-form-group>
                <b-form-group label="iFrame-høyde (kun tall)" label-for="form-iframe-height-input">
                  <b-form-input v-model="form.iframe_height" id="form-iframe-height-input" required placeholder="iFrame-høyde" ></b-form-input>
                </b-form-group>
              </div>
            </b-row>
            <b-button type="submit" size="md" variant="success" v-if="!editing">Opprett skjema</b-button>
            <b-button type="submit" size="md" variant="primary" v-if="editing">Endre skjema</b-button>
            <b-button v-on:click="abortEdit()" size="md" variant="secondary" v-if="editing">Avbryt</b-button>
          </b-form>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Skjemaer">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="forms">
            <template v-slot:cell(edit)="forms">
              <edit-button class="mx-3" @click.native="edit(forms.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(forms.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="forms">
            <template v-slot:cell(edit)="forms">
              <edit-button class="mx-3" @click.native="edit(forms.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(forms.item)"></delete-button>
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
import EditButton from '@/components/admin/EditButton.vue'
import DeleteButton from '@/components/admin/DeleteButton.vue'
export default {
  name: 'FormAdminView',
  components: {
    ImagePreview,
    EditButton,
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        'id', { key: 'external_url', label: 'Ekstern url' }, { key: 'internal_url', label: 'Intern url' },
        { key: 'iframe_height', label: 'iFrame-høyde' },
        { key: 'edit', label: '' }
      ],
      form: {
        external_url: '',
        internal_url: '',
        iframe_height: ''
      },
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
    forms: function () {
      return this.$store.state.forms.all
    },
    numBusinesses: function () {
      return this.forms.length
    }
  },
  methods: {
    handleSubmit: function () {
      axios[(this.$data.editing ? 'put' : 'post')](process.env.VUE_APP_API_HOST + '/api/form/' +
            (this.$data.editing ? this.$data.form.id + '/' : ''), this.$data.form).then((response) => {
        this.showAlert('success', 'Suksess!', 'Skjemaet er blitt ' +
           (this.$data.editing ? 'endret.' : 'lagt til.'))
        this['forms/' + (this.$data.editing ? 'updateForm' : 'addForm')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Skjemaet kunne ikke legges ut.')
      })
    },
    destroy: function (form) {
      if (!confirm('Er du sikker på at du vil slette ' + form.internal_url + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/form/' +
        form.id + '/').then((response) => {
        this.showAlert('success', 'Suksess!', 'Skjemaet er blitt slettet')
        this['forms/deleteForm'](form)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Skjemaet kunne ikke slettes.')
      })
      this.resetForm()
    },
    validateWebsiteUrl: function () {
      this.$data.form.external_url = this.validateLink(this.$data.form.external_url)
    },
    validateLink: function (link) {
      if (!(link.startsWith('https://') || link.startsWith('http://'))) {
        return 'https://'.concat(link)
      } else {
        return link
      }
    },
    resetForm: function () {
      this.$data.form = {external_url: '', internal_url: '', iframe_height: ''}
      this.$data.editing = false
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
    edit: function (form) {
      this.$data.form = form
      this.$data.editing = true
    },
    abortEdit: function () {
      this.resetForm()
      this.$data.editing = false
    },
    ...mapMutations(['forms/addForm', 'forms/deleteForm', 'forms/updateForm'])
  }
}
</script>

<style scoped lang="scss">

</style>
