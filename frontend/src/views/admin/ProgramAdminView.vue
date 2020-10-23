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
        <b-card header="Legg til 'ProgramItem' i programmet på siden" class="h-100">
          <b-form @submit.prevent="handleSubmit">
            <b-row>
              <div class="col-12 col-md-6">
                <b-form-group label="Tittel" label-for="item-header-input">
                  <b-form-input v-model="programItem.header" id="item-header-input" required placeholder="Tittel på 'ProgramItem'" ></b-form-input>
                </b-form-group>
                <b-form-group label="Sted" label-for="item-place-input">
                  <b-form-input v-model="programItem.place" id="item-place-input" placeholder="Stedet det skal foregå" ></b-form-input>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6">
                <b-form-group label="Dato" label-for="item-date-input">
                  <b-form-input type="date" v-model="programItem.date" id="item-date-input" required placeholder="Velg dato for 'ProgramItem'"></b-form-input>
                </b-form-group>
                <b-form-group label="Starttid" label-for="item-timeStart-input">
                  <b-form-input type="time" v-model="programItem.timeStart" id="item-timeStart-input" required placeholder="Velg starttid for 'ProgramItem'"></b-form-input>
                </b-form-group>
                <b-form-group label="Slutttid" label-for="item-timeEnd-input">
                  <b-form-input type="time" v-model="programItem.timeEnd" id="item-timeEnd-input" placeholder="Velg slutttid for 'ProgramItem'"></b-form-input>
                </b-form-group>
              </div>
              <div class="col-12 col-md-6 mb-2">
                <b-form-group label="Tekst" label-for="item-paragraph-input-0">
                  <div :key="index" v-for="(line,index) in programItem.paragraph" class="row mb-1 pl-2">
                      <b-form-input class="col-10 mr-1" v-model="programItem.paragraph[index]" :id="'item-paragraph-input-'+index" placeholder="Linje med brødtekst"></b-form-input>
                      <b-button class="" @click="handleDeleteParagraphLine(index)" variant="danger">
                          Slett
                      </b-button>
                  </div>
                </b-form-group>
                <b-button @click="handleAddLine">
                    Legg til tekst linje
                </b-button>
              </div>
              <div class="col-12 mt-2 mb-3">
                <b-form-checkbox
                    id="checkbox-registration"
                    v-model="programItem.registration"
                    name="checkbox-registration">
                  Påmelding
                </b-form-checkbox>
              </div>
                <div class="col-12 col-md-6" v-if="programItem.registration">
                    <b-form-group label="Dato for påmeldingsstart" label-for="item-date-registration-start-input">
                      <b-form-input type="date" v-model="programItem.registrationStartDate" id="item-date-registration-start-input" :required="programItem.registration"></b-form-input>
                    </b-form-group>
                    <b-form-group label="Tid for påmeldingsstart" label-for="item-time-registration-start-input">
                      <b-form-input type="time" v-model="programItem.registrationStartTime" id="item-time-registration-start-input" :required="programItem.registration"></b-form-input>
                    </b-form-group>
                </div>
                <div class="col-12 col-md-6" v-if="programItem.registration">
                  <b-form-group label="Dato for påmeldingsslutt" label-for="item-date-registration-end-input">
                    <b-form-input type="date" v-model="programItem.registrationEndDate" id="item-date-registration-end-input"></b-form-input>
                  </b-form-group>
                  <b-form-group label="Tid for påmeldingsslutt" label-for="item-time-registration-end-input">
                    <b-form-input type="time"  v-model="programItem.registreationEndTime" id="item-time-registration-end-input"></b-form-input>
                  </b-form-group>
                </div>
                <div class="col-12 col-md-6 mt-3" v-if="programItem.registration">
                  <b-form-group label="Max antall påmeldte" label-for="item-max-registred-input">
                    <b-form-input type="number" v-model="programItem.maxRegistered" id="item-max-registered-input"></b-form-input>
                  </b-form-group>
                </div>
                <div class="col-12 col-md-6 mt-3" v-if="programItem.registration">
                  <b-form-group label="Email som avmeldingsmail blir sendt til" label-for="item-email-input">
                    <b-form-input type="email" v-model="programItem.cancelEmail" id="item-email-input" :required="programItem.registration" placeholder="Email til ansvarlig" ></b-form-input>
                </b-form-group>
                </div>
            </b-row>
            <b-button type="submit" size="md" variant="success" v-if="!editing">Legg ut programItem</b-button>
            <b-button type="submit" size="md" variant="primary" v-if="editing">Endre programItem</b-button>
            <b-button v-on:click="abortEdit()" size="md" variant="secondary" v-if="editing">Avbryt</b-button>
          </b-form>
        </b-card>
      </div>
    </b-row>
    <b-row>
      <div class="col-12">
        <b-card header="Teammedlemmer">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="programItems">
            <template slot="edit" slot-scope="programItems">
              <edit-button class="mx-3" @click.native="edit(programItems.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(programItems.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="programItems">
            <template slot="edit" slot-scope="programItems">
              <edit-button class="mx-3" @click.native="edit(programItems.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(programItems.item)"></delete-button>
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
  name: 'TeamMemberAdminView',
  components: {
    EditButton,
    DeleteButton
  },
  data: function () {
    return {
      programItems: [],
      fields: [
        'id', { key: 'header', label: 'Header' }, { key: 'paragraph', label: 'Text' },
        { key: 'place', label: 'Place' }, { key: 'timeStart', label: 'Staring time' },
        { key: 'timeEnd', label: 'Ending time' }, { key: 'edit', label: '' }
      ],
      programItem: {
        header: '',
        paragraph: [''],
        place: '',
        date: '',
        timeStart: '',
        timeEnd: '',
        registration: false,
        registered: 0,
        maxRegistered: 0,
        registrationStartDate: '',
        registrationStartTime: '',
        registreationEndDate: '',
        registreationEndTime: '',
        cancelEmail: ''
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
    program: function () {
      //return program from database
      //return this.$store.state.teamMembers.all
    },
  },
  methods: {
    handleAddLine: function () {
      console.log(this.$data.programItem.timeStart)
      if (this.$data.programItem.paragraph[this.$data.programItem.paragraph.length -1] !== '') {
        this.$data.programItem.paragraph.push('')
      }
    },
    handleDeleteParagraphLine: function (index) {
      let para = this.$data.programItem.paragraph
      this.$data.programItem.paragraph = para.slice(0,index).concat(para.slice(index+1, para.length))
    },
    handleSubmit: function () {
      
    },
    destroy: function (teamMember) {
     
    },
    resetForm: function () {
      this.$data.programItem = {
        header: '',
        paragraph: [''],
        place: '',
        date: new Date(),
        timeStart: new Date(),
        timeEnd: new Date(),
        registration: false,
        registered: 0,
        maxRegistered: 0,
        registrationStartDate: new Date(),
        registrationStartTime: new Date(),
        registreationEndDate: new Date(),
        registreationEndTime: new Date(),
        cancelEmail: ''
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
    edit: function (item) {
      this.$data.programItem = item
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
