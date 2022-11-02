<template>
  <div class="participants-admin-view">
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
        <b-card header="Velg event og se deltagere" class="h-100">
            <b-form-select v-model="selectedEvent" :options="events"></b-form-select>
            <b-link :href="'mailto:' +concatEmails">{{'Send mail til alle deltagere'}}</b-link>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Participants">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="filteredList">
            <template v-slot:cell(delete)="filteredList">
              <delete-button class="mx-3" @click.native="destroy(filteredList.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="filteredList">
            <template v-slot:cell(delete)="filteredList" >
              <delete-button class="mx-3" @click.native="destroy(filteredList.item)"></delete-button>
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
import DeleteButton from '@/components/admin/DeleteButton.vue'
export default {
  name: 'ParticipantAdminView',
  components: {
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        'id', {key: 'name', label: 'Navn'}, {key: 'study', label: 'Studie'}, {key: 'year', label: 'Årskull'}, {key: 'email', label: 'Email'}, { key: 'delete', label: '' }
      ],
      alert: {
        dismissSecs: 5,
        dismissCountDown: 0,
        variant: 'info',
        heading: '',
        message: ''
      },
      selectedEvent: 1,
      participantList: []
    }
  },
  computed: {
    events: function () {
      let program = this.$store.state.program.all
      let options = []
      program.forEach(event => {
        options.push(
          {
            value: event.id, text: event.header
          }
        )
      })
      return options
    },
    filteredList: function () {
      let participants = this.$store.state.participant.all
      this.setParticipantList(participants)
      return participants.filter(par => par.event === this.$data.selectedEvent)
    },
    concatEmails: function () {
      let emailString = ''
      this.$data.participantList.forEach((participant) => {
        if (participant.event === this.$data.selectedEvent) {
          emailString += participant.email + ';'
        }
      })
      return emailString
    }
  },
  methods: {
    setParticipantList: function (participants) {
      this.$data.participantList = participants
    },
    destroy: function (participant) {
      if (!confirm('Er du sikker på at du vil slette ' + participant.name + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/participant/' +
        participant.id + '/').then((response) => {
        this.showAlert('success', 'Suksess!', 'Participant er blitt slettet')
        this['participant/deleteParticipant'](participant)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'Participant kunne ikke slettes.')
      })
    },
    showAlert: function (variant, heading, message) {
      this.alert.variant = variant
      this.alert.heading = heading
      this.alert.message = message
      this.alert.dismissCountDown = this.alert.dismissSecs
      window.scrollTo({top: 0, behavior:'smooth'})
    },
    countDownChanged: function (dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    },
    ...mapMutations(['participant/addParticipant', 'participant/deleteParticipant',
      'participant/updateParticipant'])
  }
}
</script>

<style lang="scss" scoped>

</style>
