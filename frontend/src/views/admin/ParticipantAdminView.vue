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
            <b-link :href="'mailto:' +concatEmails">{{$t('sendtoall')}}</b-link>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Deltakere">
          <b-link download="Deltakere.csv" :href="participantsDownloadHref"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'download' }"/> Last ned CSV</b-link>
          <b-table class="d-none d-md-table" hover :fields="fields" :items="participantList">
            <template v-slot:cell(delete)="participantList">
              <delete-button class="mx-3" @click.native="destroy(participantList.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="participantList">
            <template v-slot:cell(delete)="participantList" >
              <delete-button class="mx-3" @click.native="destroy(participantList.item)"></delete-button>
            </template>
          </b-table>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Venteliste">
          <b-link download="Deltakere.csv" :href="waitinglistDownloadHref"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'download' }"/> Last ned CSV</b-link>
          <b-table class="d-none d-md-table" hover :fields="fields" :items="waitingList">
            <template v-slot:cell(delete)="waitingList">
              <delete-button class="mx-3" @click.native="destroy(waitingList.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="waitingList">
            <template v-slot:cell(delete)="waitingList" >
              <delete-button class="mx-3" @click.native="destroy(waitingList.item)"></delete-button>
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

function generateDownloadableCsv (headerRow, rows) {
  let csvContent = 'data:text/csv;charset=utf-8,'

  csvContent += headerRow.join(',') + '\r\n'

  rows.forEach(rowArray => {
    let row = rowArray.join(',')
    csvContent += row + '\r\n'
  })

  return encodeURI(csvContent)
}

export default {
  name: 'ParticipantAdminView',
  components: {
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        'id',
        {key: 'name', label: 'Navn'},
        {key: 'study', label: 'Studie'},
        {key: 'year', label: 'Årskull'},
        {key: 'email', label: 'Email'},
        {key: 'allergies', label: 'Allergier'},
        {key: 'delete', label: ''}
      ],
      alert: {
        dismissSecs: 5,
        dismissCountDown: 0,
        variant: 'info',
        heading: '',
        message: ''
      },
      selectedEvent: {
        id: 1,
        header: '',
        maxRegistered: 0
      }
    }
  },
  computed: {
    events: function () {
      let program = this.$store.state.program.all
      let options = []
      program.forEach(event => {
        options.push(
          {
            value: event, text: event.header
          }
        )
      })
      return options
    },
    participants: function () {
      let participants = this.$store.state.participant.all

      let filteredParticipants = participants.filter(par => par.event === this.$data.selectedEvent.id)
      let sortedParticipants = filteredParticipants.sort((a, b) => {
        return a.id - b.id
      })

      return sortedParticipants
    },
    participantList: function () {
      return this.participants.slice(0, this.$data.selectedEvent.maxRegistered)
    },
    waitingList: function () {
      return this.participants.slice(this.$data.selectedEvent.maxRegistered)
    },
    concatEmails: function () {
      let emailString = ''
      this.participants.forEach((participant) => {
        emailString += participant.email + ';'
      })
      return emailString
    },
    participantsDownloadHref: function () {
      const rows = this.participantList.map(participant => [
        participant.name,
        participant.email,
        participant.study,
        participant.year,
        participant.allergies
      ])
      return generateDownloadableCsv(['Navn', 'E-post', 'Studie', 'Årskull', 'Allergier'], rows)
    },
    waitinglistDownloadHref: function () {
      const rows = this.waitingList.map(participant => [
        participant.name,
        participant.email,
        participant.study,
        participant.year,
        participant.allergies
      ])
      return generateDownloadableCsv(['Navn', 'E-post', 'Studie', 'Årskull', 'Allergier'], rows)
    }
  },
  methods: {
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
