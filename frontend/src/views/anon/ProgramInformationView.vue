<template>
  <div>
    <h1 class="text-center">Title</h1>
    <div class="container">
      <div class="two-thirds">
        <h1 class="text-center">{{ spi.header }}</h1>
        <p v-for="paragraph in spi.paragraph">
          {{ paragraph }}
        </p>
      </div>
      <div class="one-third">
        <div class="sub-box">
          <h3>Påmelding</h3>
          <p>{{ formatDate(new Date(spi.registrationStart)) }} - {{ formatDate(new
            Date(spi.registrationEnd)) }}</p>
          <p>{{ spi.registered }}/{{ spi.maxRegistered }}</p>
          <p>{{ spi.registration }}</p>
          <p>Enable registration: {{ enableRegistration }}</p>
          <div v-if="spi.registration && spi.cancelEmail">
            <b-link @click.native="destroy_participant(name)">{{ $t('destroypart') }}</b-link>
          </div>
          <div v-if="spi.registration">
            <div v-if="submitted">
              <div>{{ $t('submitted') }}</div>
            </div>
            <div v-else-if="enableRegistration && spi.registered < spi.maxRegistered">
              <div>{{ $t('påmeldingstart') }}</div>
            </div>
            <div v-else-if="enableRegistration && spi.registered >= spi.maxRegistered">
              <div>{{ $t('vilbliventeliste') }}</div>
            </div>
            <div v-else-if="spi.afterRegistration">
              <div>{{ $t('regfinish') }}</div>
            </div>
            <div v-else>
              <div>{{ $t('regtobegin') + ' ' + formatDate(spi.registrationStart) }}</div>
            </div>
          </div>
          <div v-if="spi.registration" class='button'>
            <b-button v-if="enableRegistration && !submitted" variant='primary'
              @click="openDialog">{{ $t('påmelding') }}</b-button>
            <b-button v-else disabled variant="dark">{{ $t('påmelding') }}</b-button>
          </div>
        </div>
        <div class="sub-box">
          <p>Content for the second 1/3 sub-box</p>
        </div>
        <div class="sub-box">
          <p>Content for the third 1/3 sub-box</p>
        </div>
      </div>
    </div>
    <div>
      <b-modal :id="'dialogForm' + spi.name" :title="'Meld deg på: ' + spi.header" v-model="show" centered>
        <b-form>
          <b-form-group :id="'input-group-name' + spi.name" :label-for="'input-name' + spi.name"
            description='Skriv inn navnet ditt slik at vi vet hvem som melder seg på'>
            <b-form-input :id="'input-name' + spi.name" v-model="form.name" required placeholder='Navn'></b-form-input>
          </b-form-group>
          <b-form-group :id="'input-group-email' + spi.name" :label-for="'input-email' + spi.name"
            description='Skriv inn emailen din slik at vi kan sende deg en email for påmelding.'>
            <b-form-input :id="'input-email' + spi.name" type="email" v-model="form.email" required
              placeholder='E-post'></b-form-input>
          </b-form-group>
          <b-form-group :id="'input-group-study' + spi.name" :label-for="'input-study' + spi.name"
            description='Skriv inn det du studerer.'>
            <b-form-input :id="'input-study' + spi.name" v-model="form.study" required placeholder='Study'></b-form-input>
          </b-form-group>
          <b-form-group :id="'input-group-year' + spi.name" :label-for="'input-year' + spi.name"
            description='Skriv inn hvilket år du er på.'>
            <b-form-input :id="'input-year' + spi.name" v-model="form.year" required placeholder='Year'></b-form-input>
          </b-form-group>
        </b-form>
        <template v-slot:modal-footer>
          <div>
            <b-button variant='outline-secondary' @click="onCancel">
              Avbryt
            </b-button>
            <b-button variant='primary' @click="onSubmit">
              Meld på
            </b-button>
          </div>
        </template>
      </b-modal>
    </div>
  </div>
</template>

<!-- <ProgramItem :timeStart="spi.timeStart" :timeEnd="spi.timeEnd" :place="spi.place" :header="spi.header"
              :paragraph="spi.paragraph" :registration="spi.registration" :maxRegistered="spi.maxRegistered"
              :registered="spi.registered" :cancelEmail="spi.cancelEmail" :registrationStart="spi.registrationStart"
              :registrationEnd="spi.registrationEnd" :name="spi.id">
            </ProgramItem> -->



<script>
import axios from 'axios'
import ProgramItem from '@/components/anon/ProgramItem.vue'
// import other dependencies if needed

export default {
  components: {
    ProgramItem,
    // other components if needed
  },
  data() {
    return {
      form: {
        email: '',
        name: '',
        study: '',
        year: ''
      },
      show: false,
      submitted: false
    }
  },
  methods: {
    // formatDate(dateObj) {
    //   let months = ['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'desember']
    //   let date = dateObj.getDate()
    //   let month = dateObj.getMonth()
    //   return String(date) + '. ' + months[month]
    // },
    formatTime(dateObj) {
      let hours = dateObj.getHours()
      let minutes = dateObj.getMinutes()
      hours = (hours > 9) ? String(hours) : ('0' + String(hours))
      minutes = (minutes > 9) ? String(minutes) : ('0' + String(minutes))
      return hours + ':' + minutes
    },
    formatDate(dateObj) {
      let day = dateObj.getDate()
      let month = dateObj.getMonth() + 1
      let year = dateObj.getFullYear()
      day = (day > 9) ? String(day) : ('0' + String(day))
      month = (month > 9) ? String(month) : ('0' + String(month))
      return this.formatTime(dateObj) + ' ' + day + '.' + month + '.' + year
    },
    openDialog() {
      this.$data.form = { email: '', name: '', study: '', year: '' }
      this.$data.show = true
    },
    onSubmit(e) {
      e.preventDefault()
      let data = this.$data.form
      // Generate and include 6-character random deregistering code
      data.code = Array(6).fill(0).map(x => Math.random().toString(36).charAt(2)).join('').toUpperCase()
      if (this.checkValidForm(data)) {
        this.submitForm()
        // Clear data
        this.$data.show = false
        this.$data.form = { email: '', name: '', study: '', year: '' }
        this.$data.submitted = true
      }
    },
    submitForm() {
      axios.post(process.env.VUE_APP_API_HOST +
        '/api/participant/', { event: this.spi.name, ...this.spi.form })
        .then((response) => console.log(response))
        .catch((e) => {
          console.log('Error in submitForm')
          console.log(e)
        })
    },
    onCancel(e) {
      e.preventDefault()
      this.$data.form = { email: '', name: '', study: '', year: '' }
      this.$data.show = false
    },
    checkValidForm(check) {
      for (let key in check) {
        if (check[key] === '') {
          return false
        } else if (key === 'email') {
          let at = check[key].split('@')
          let dot = at[at.length - 1].split('.')
          if (at.length < 2 || dot.length < 2 || dot[dot.length - 1].length === 0) {
            return false
          }
        }
      }
      return true
    },
    nameUrlEncoded: function (header) {
      return encodeURIComponent(header)
    },
    destroy_participant: function (event) {
      let email = prompt('Vennligst skriv inn emailen din:')
      let participants = this.$store.state.participant.all
      let participant = participants.filter(par => par.email === email && par.event === event)[0]

      if (participant !== undefined) {
        // Send deregistering code
        let code = participant.code
        axios.get(process.env.VUE_APP_API_HOST + '/api/participant/' +
          participant.id + '/').then(_ => {
            // Prompt user for code, and delete participant if input matches
            let retry = true
            while (retry) {
              let inputedCode = prompt('Vennligst skriv inn koden som ble sendt til ' + participant.email + '. Hvis du ikke mottar mailen, vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
              if (inputedCode === code) {
                if (confirm('Er du sikker på at du vil melde av ' + participant.name + '?')) {
                  axios.delete(process.env.VUE_APP_API_HOST + '/api/participant/' +
                    participant.id + '/').then(_ => {
                      alert(participant.name + ' er nå avmeldt.')
                    }).catch(_ => {
                      alert('Det oppsto en feil under avmeldingen. Vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
                    })
                }
                break
              } else {
                retry = confirm('Feil kode. Vil du prøve igjen?')
              }
            }
          }).catch(_ => {
            alert('Det oppsto en feil under sendingen av avmeldingskoden. Vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
          })
      } else if (email !== null) {
        alert('Fant ingen deltakere med denne epost-adressen på dette arrangementet.')
      }
    }
  },
  // methods, computed properties, etc.
  computed: {
    spi: function () {
      let programReferer = this.$route.params.programReferer
      let prog = this.$store.getters['program/anonProgram']
      return prog.find(item => this.nameUrlEncoded(item.header) === programReferer)
    },
    registered: function () {
      return this.$store.state.participant.all.filter(par => par.event === this.spi.name).length
    },
    beforeRegistration: function () {
      let now = new Date()
      return this.spi.registrationStart.getTime() > now.getTime()
    },
    afterRegistration: function () {
      let now = new Date()
      if (this.spi.registrationEnd) {
        return this.spi.registrationEnd.getTime() < now.getTime()
      }
      return this.spi.timeStart.getTime() < now.getTime()
    },
    enableRegistration: function () {
      if (!this.spi.registration) {
        console.log('Registration not enabled')
        return false
      }
      if (this.beforeRegistration) {
        console.log('Registration not enabled')
        return false
      }
      if (this.afterRegistration) {
        console.log('Registration not enabled')
        return false
      }
      return true
    },
  }
}
</script>



<style scoped lang="scss">
.container {
    display: flex;
    width: 100%;
}

.card {
    position: relative;
    border-radius: 20px;
    border-width: 2px;
    border-color: var(--line-border-color);
    background-color: white;
}

.two-thirds {
  flex: 2;
  background-color: white;
  padding: 10px;
  /* Reduce padding for better space management */
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.one-third {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 10px;
  /* Reduce padding for better space management */
  overflow-y: auto;
  /* Enable vertical scrolling if content exceeds box height */
  max-height: 100%;
  /* Set a maximum height for the box */
}

.sub-box {
  flex: 1;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 10px;
  /* Reduce padding for better space management */
  margin-bottom: 10px;
  overflow-y: auto;
  /* Enable vertical scrolling if content exceeds box height */
}
</style>
