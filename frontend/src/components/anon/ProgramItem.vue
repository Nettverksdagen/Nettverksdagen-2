<template>
  <div>
    <div class="timeline-item">
      <div class="timestamp">
        <h4><span class="font-weight-bold">{{ formatTime(timeStart) }}</span></h4>
      </div>
      <div class="card">
        <div class="card-body">
          <div class="header">
            <div v-if="header">
              <router-link :to="{ name: 'ProgramDetails', params: { programReferer: nameUrlEncoded } }">
                <div class="businessContainer">
                  <p class='description'>{{ header }}</p>
                </div>
              </router-link>
            </div>
            <div v-if="registration && maxRegistered">
              <h5 v-if="registered <= maxRegistered">
                {{ registered + '/' + maxRegistered + ' ' + $t('påmeldte') }}
              </h5>
              <h5 v-else>
                {{ maxRegistered + ' ' + $t('påmeldte') + ', ' + (registered - maxRegistered) + ' ' + $t('onthe') + ' '
                  + $t('venteliste') }}
              </h5>
            </div>
          </div>
          <div v-if="paragraph">
            <div :key="name + line" v-for="line in paragraph">
              <p class='description'>{{ line }}</p>
            </div>
          </div>
          <div v-if="registration" class='button'>
            <b-button v-if="enableRegistration && !submitted" variant='primary'
              @click="openDialog">{{ $t('påmelding') }}</b-button>
            <b-button v-else disabled variant="dark">{{ $t('påmelding') }}</b-button>
          </div>
          <div class="footer">
            <div class="inline">
              <div v-if="place" class="d-block d-md-inline">
                <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1" />
                <div v-html="place" class="d-inline" />
              </div>
              <div v-if="timeEnd" class="d-inline">
                <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-md-1 ml-md-2" />
                {{ formatTime(timeStart) }} - {{ formatTime(timeEnd) }}
              </div>
            </div>
            <div v-if="registration && cancelEmail">
              <b-link @click.native="destroy_participant(name)">{{ $t('destroypart') }}</b-link>
            </div>
            <div v-if="registration">
              <div v-if="submitted">
                <div>{{ $t('submitted') }}</div>
              </div>
              <div v-else-if="enableRegistration && registered < maxRegistered">
                <div>{{ $t('påmeldingstart') }}</div>
              </div>
              <div v-else-if="enableRegistration && registered >= maxRegistered">
                <div>{{ $t('vilbliventeliste') }}</div>
              </div>
              <div v-else-if="afterRegistration">
                <div>{{ $t('regfinish') }}</div>
              </div>
              <div v-else>
                <div>{{ $t('regtobegin') + ' ' + formatDate(registrationStart) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <b-modal :id="'dialogForm' + name" :title="'Meld deg på: ' + header" v-model="show" centered>
        <b-form>
          <b-form-group :id="'input-group-name' + name" :label-for="'input-name' + name"
            description='Skriv inn navnet ditt slik at vi vet hvem som melder seg på'>
            <b-form-input :id="'input-name' + name" v-model="form.name" required placeholder='Navn'></b-form-input>
          </b-form-group>
          <b-form-group :id="'input-group-email' + name" :label-for="'input-email' + name"
            description='Skriv inn emailen din slik at vi kan sende deg en email for påmelding.'>
            <b-form-input :id="'input-email' + name" type="email" v-model="form.email" required
              placeholder='E-post'></b-form-input>
          </b-form-group>
          <b-form-group :id="'input-group-study' + name" :label-for="'input-study' + name"
            description='Skriv inn det du studerer.'>
            <b-form-input :id="'input-study' + name" v-model="form.study" required placeholder='Study'></b-form-input>
          </b-form-group>
          <b-form-group :id="'input-group-year' + name" :label-for="'input-year' + name"
            description='Skriv inn hvilket år du er på.'>
            <b-form-input :id="'input-year' + name" v-model="form.year" required placeholder='Year'></b-form-input>
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

<script>
import axios from 'axios'
// import { mapMutations } from 'vuex'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMapMarkerAlt, faClock } from '@fortawesome/free-solid-svg-icons'

library.add(faMapMarkerAlt, faClock)
export default {
  name: 'ProgramItem',
  props: ['timeStart', 'timeEnd', 'place', 'header', 'paragraph', 'registration', 'maxRegistered', 'cancelEmail', 'registrationStart', 'registrationEnd', 'name'],
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
  computed: {
    registered: function () {
      return this.$store.state.participant.all.filter(par => par.event === this.$props.name).length
    },
    beforeRegistration: function () {
      let now = new Date()
      return this.$props.registrationStart.getTime() > now.getTime()
    },
    afterRegistration: function () {
      let now = new Date()
      if (this.$props.registrationEnd) {
        return this.$props.registrationEnd.getTime() < now.getTime()
      }
      return this.$props.timeStart.getTime() < now.getTime()
    },
    enableRegistration: function () {
      if (!this.$props.registration) {
        return false
      }
      if (this.beforeRegistration) {
        return false
      }
      if (this.afterRegistration) {
        return false
      }
      return true
    }
  },
  methods: {
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
      console.log({ event: this.$props.name, ...this.$data.form })
      axios.post(process.env.VUE_APP_API_HOST +
        '/api/participant/', { event: this.$props.name, ...this.$data.form })
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
  }
}
</script>

<style scoped lang="scss">
.card {
  position: relative;
  border-radius: 20px;
  border-width: 2px;
  border-color: var(--line-border-color);
  background-color: white;
}

.numberofpeople {
  display: inline;
}

.timeline-item {
  padding: 15px 0 15px 40px;
  position: relative;
  background-color: inherit;
  width: 100%;
}

/* Add arrows to the right container (pointing left) */
.timeline-item::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  left: 30px;
  border-width: 10px 10px 10px 0;
  border-color: transparent white transparent transparent;
}

/* The circles on the timeline */
.timeline-item::after {
  content: '';
  position: absolute;
  width: 25px;
  height: 25px;
  right: -17px;
  background-color: white;
  border: 4px solid var(--primary-color);
  top: 18px;
  border-radius: 50%;
  z-index: 1;
  left: -13px;
}

.header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 20px;
  overflow-wrap: break-word;

  @media(min-width: 992px) {
    flex-direction: row;
    margin-bottom: 0;
  }
}

.footer {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 0px;

  @media(min-width: 992px) {
    flex-direction: row;
    margin-bottom: 0;
  }
}

.button {
  display: flex;
  flex-direction: row;
  margin-bottom: 10px;

  @media(min-width: 768px) {
    margin-right: 15px;
    flex-direction: row-reverse;
  }
}

.timestamp {
  position: absolute;
  left: -82px;
  top: 16px;
}

.description {
  font-size: 1.1em;
}

/deep/ .modal-content {
  border: none;
  border-radius: 20px;
  background-color: var(--line-border-color);
  color: black;
}

/deep/ .modal-header {
  border-bottom: none;
}

/deep/ .modal-footer {
  border: none;
}

/deep/ .modal-title {
  text-align: center;
  width: 100%;
}

@media(max-width: 768px) {
  .timestamp {
    top: 30px;

    h4 {
      font-size: 1.2em;
    }
  }

  .timeline-item::after {
    top: 30px;
    left: -30px;
  }

  .timeline-item {
    padding-left: 16px;
  }

  .timeline-item::before {
    left: 8px;
    top: 32px;
  }
}
</style>
