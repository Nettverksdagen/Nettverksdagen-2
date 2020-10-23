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
                    <b-form-input type="time"  v-model="programItem.registrationEndTime" id="item-time-registration-end-input"></b-form-input>
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
        <b-card header="Program">
          <b-table class="d-none d-md-table" hover :fields="fields" :items="program">
            <template slot="edit" slot-scope="program">
              <edit-button class="mx-3" @click.native="edit(program.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(program.item)"></delete-button>
            </template>
          </b-table>
          <b-table class="d-block d-md-none" stacked :fields="fields" :items="program">
            <template slot="edit" slot-scope="program">
              <edit-button class="mx-3" @click.native="edit(program.item)"></edit-button>
              <delete-button class="mx-3" @click.native="destroy(program.item)"></delete-button>
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
  name: 'ProgramAdminView',
  components: {
    EditButton,
    DeleteButton
  },
  data: function () {
    return {
      fields: [
        'id',{ key: 'header', label: 'Header' }, { key: 'paragraph', label: 'Text' },
        { key: 'place', label: 'Place' }, { key: 'timeStart', label: 'Staring time' },
        { key: 'timeEnd', label: 'Ending time' }, { key: 'Edit', label: '' }
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
        registrationEndDate: '',
        registrationEndTime: '',
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
      return this.$store.getters['program/adminProgram']
    },
  },
  methods: {
    formatProgramItem: function(programItem) {
      let newItem = {};
      if (this.$data.editing) {
        newItem.id = programItem.id;
      }      
      let fields = ['header', 'paragraph', 'place', 'registration'];
      fields.forEach((field) => {
        newItem[field] = programItem[field];
      })

      let date = programItem.date.split('-')
      let timeStart = programItem.timeStart.split(':')
      newItem.timeStart = new Date(Number(date[0]), Number(date[1]), Number(date[2]), Number(timeStart[0]), Number(timeStart[1]),0,0).getTime();
      if (programItem.timeEnd) {
        let timeEnd = programItem.timeEnd.split(':')
        newItem.timeEnd = new Date(Number(date[0]), Number(date[1]), Number(date[2]), Number(timeEnd[0]), Number(timeEnd[1]),0,0).getTime();
      } else {
        newItem.timeEnd = undefined
      }
      

      if (newItem.registration) {
        let registrationFields = ['maxRegistered', 'registered', 'cancelEmail']
        registrationFields.forEach((field) => {
          newItem[field] = programItem[field]
        })
        let registrationStartDate = programItem.registrationStartDate.split('-')
        let registrationStartTime = programItem.registrationStartTime.split(':')
        newItem.registrationStart = new Date(Number(registrationStartDate[0]), Number(registrationStartDate[1]), Number(registrationStartDate[2]), 
        Number(registrationStartTime[0]), Number(registrationStartTime[1]),0,0).getTime();
        
       console.log(!!programItem.registrationEndDate, !!programItem.registrationEndTime)
        if (!!programItem.registrationEndDate && !!programItem.registrationEndTime) {
          let registrationEndDate = programItem.registrationEndDate.split('-')
          let registrationEndTime = programItem.registrationEndTime.split(':')
          newItem.registrationEnd = new Date(Number(registrationEndDate[0]), Number(registrationEndDate[1]), Number(registrationEndDate[2]), 
          Number(registrationEndTime[0]), Number(registrationEndTime[1]),0,0).getTime();
        } else {
          newItem.registrationEnd = undefined
        }
      } else {
        let registrationFields = ['maxRegistered', 'registered', 'cancelEmail', 'registrationStart', 'registrationEnd']
        registrationFields.forEach((field) => {
          newItem[field] = undefined
        })
      }      
      return newItem
    },
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
      let programItem = this.formatProgramItem(this.$data.programItem);
      axios[(this.$data.editing ? 'put' : 'post')](process.env.VUE_APP_API_HOST +
        '/api/program/' + (this.$data.editing ? programItem + '/' : ''),
      programItem).then((response) => {
        this.showAlert('success', 'Suksess!', 'ProgramItem har blitt' +
          (this.$data.editing ? 'endret.' : 'lagt ut på forsiden.'))
        this['program/' + (this.$data.editing ? 'updateProgramItem' : 'addProgramItem')](response.data)
        this.resetForm()
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'ProgramItem kunne ikke legges ut.')
      })
    },
    destroy: function (programItem) {
     if (!confirm('Er du sikker på at du vil slette ' + programItem.header + '?')) {
        return
      }
      axios.delete(process.env.VUE_APP_API_HOST + '/api/program/' +
        programItem.id + '/').then((response) => {
        this.showAlert('success', 'Suksess!', 'ProgramItem er blitt slettet')
        this['program/deleteProgramItem'](programItem)
      }).catch((e) => {
        this.showAlert('danger',
          'Error ' + e.response.status + ' ' + e.response.statusText,
          'ProgramItem kunne ikke slettes.')
      })
      this.resetForm()
    },
    resetForm: function () {
      this.$data.programItem = {
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
      this.$data.editing = true
    },
    abortEdit: function () {
      this.resetForm()
      this.$data.editing = false
    },
    ...mapMutations(['program/addProgramItem', 'program/deleteProgramItem',
      'program/updateProgramItem'])
  }
}
</script>

<style lang="scss" scoped>

</style>
