<template>
  <div class="faq-admin-view">
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
        <b-card :header="$t('admin.faq.header')" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <h5 class="mt-3 mb-3">Norsk</h5>
            <b-form-group :label="$t('admin.faq.questionNorwegian')" label-for="question-nb-input">
              <b-form-input
                id="question-nb-input"
                v-model="faq.question_nb"
                :placeholder="$t('admin.faq.questionNorwegianPlaceholder')"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group :label="$t('admin.faq.answerNorwegian')" label-for="answer-nb-input">
              <b-form-textarea
                id="answer-nb-input"
                v-model="faq.answer_nb"
                :placeholder="$t('admin.faq.answerNorwegianPlaceholder')"
                rows="4"
                required
              ></b-form-textarea>
            </b-form-group>

            <hr>

            <h5 class="mt-3 mb-3">English</h5>
            <b-form-group :label="$t('admin.faq.questionEnglish')" label-for="question-en-input">
              <b-form-input
                id="question-en-input"
                v-model="faq.question_en"
                :placeholder="$t('admin.faq.questionEnglishPlaceholder')"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group :label="$t('admin.faq.answerEnglish')" label-for="answer-en-input">
              <b-form-textarea
                id="answer-en-input"
                v-model="faq.answer_en"
                :placeholder="$t('admin.faq.answerEnglishPlaceholder')"
                rows="4"
                required
              ></b-form-textarea>
            </b-form-group>

            <hr>

            <b-form-group :label="$t('admin.faq.order')" label-for="order-input">
              <b-form-input
                id="order-input"
                v-model.number="faq.order"
                type="number"
                :placeholder='0'
              ></b-form-input>
            </b-form-group>

            <b-button type="submit" size="md" variant="success" v-if="!editing">{{ $t('leggut') }}</b-button>
            <b-button type="submit" size="md" variant="primary" v-if="editing">{{ $t('edit') }}</b-button>
            <b-button v-if="editing" @click="abortEdit" size="md" variant="secondary">{{ $t('abort') }}</b-button>
          </b-form>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card :header="$t('admin.faq.listHeader')">
          <b-table striped hover :items="faqs" :fields="fields">
            <template #cell(question_nb)="data">
              <div class="text-truncate" style="max-width: 200px;">{{ data.value }}</div>
            </template>
            <template #cell(question_en)="data">
              <div class="text-truncate" style="max-width: 200px;">{{ data.value }}</div>
            </template>
            <template #cell(answer_nb)="data">
              <div class="text-truncate" style="max-width: 200px;">{{ data.value }}</div>
            </template>
            <template #cell(answer_en)="data">
              <div class="text-truncate" style="max-width: 200px;">{{ data.value }}</div>
            </template>
            <template #cell(edit)="data">
              <EditButton @click.native="edit(data.item)" />
              <DeleteButton @click.native="destroy(data.item)" />
            </template>
          </b-table>
        </b-card>
      </div>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios'
import { mapMutations } from 'vuex'
import EditButton from '@/components/admin/EditButton.vue'
import DeleteButton from '@/components/admin/DeleteButton.vue'

export default {
  name: 'FAQAdminView',
  components: {
    EditButton,
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        { key: 'id', label: 'ID' },
        { key: 'question_nb', label: this.$t('admin.faq.questionNorwegian') },
        { key: 'question_en', label: this.$t('admin.faq.questionEnglish') },
        { key: 'answer_nb', label: this.$t('admin.faq.answerNorwegian') },
        { key: 'answer_en', label: this.$t('admin.faq.answerEnglish') },
        { key: 'order', label: this.$t('admin.faq.order') },
        { key: 'edit', label: '' }
      ],
      faq: {
        question_nb: '',
        question_en: '',
        answer_nb: '',
        answer_en: '',
        order: 0
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
    faqs: function () {
      return this.$store.state.faq.all
    }
  },
  created() {
    this.$store.dispatch('faq/fetchFAQs')
  },
  methods: {
    handleSubmit: function () {
      axios[this.$data.editing ? 'put' : 'post'](
        process.env.VUE_APP_API_HOST + '/api/faq/' + 
        (this.$data.editing ? this.$data.faq.id + '/' : ''),
        this.$data.faq
      ).then((response) => {
        this.showAlert('success', this.$t('admin.success'), 'FAQ ' + 
          (this.$data.editing ? this.$t('admin.updated') : this.$t('admin.created')))
        this['faq/' + (this.$data.editing ? 'updateFAQ' : 'addFAQ')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'FAQ ' + this.$t('admin.couldNotPublish'))
      })
    },
    destroy: function (faq) {
      if (!confirm(this.$t('admin.confirmDelete') + ' FAQ #' + faq.id + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/faq/' + faq.id + '/').then((response) => {
        this.showAlert('success', this.$t('admin.success'), 'FAQ ' + this.$t('admin.deleted'))
        this['faq/deleteFAQ'](faq)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'FAQ ' + this.$t('admin.couldNotDelete'))
      })
      this.resetForm()
    },
    resetForm: function () {
      this.$data.faq = {
        question_nb: '',
        question_en: '',
        answer_nb: '',
        answer_en: '',
        order: 0
      }
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
    edit: function (faq) {
      this.$data.faq = faq
      this.$data.editing = true
      window.scrollTo({top: 0, behavior: 'smooth'})
    },
    abortEdit: function () {
      this.resetForm()
      this.$data.editing = false
    },
    ...mapMutations(['faq/addFAQ', 'faq/deleteFAQ', 'faq/updateFAQ'])
  }
}
</script>

<style scoped lang="scss">
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
