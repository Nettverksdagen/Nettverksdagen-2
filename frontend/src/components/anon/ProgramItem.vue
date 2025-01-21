<template>
<div>
  <div class="timeline-item" @click="$emit('click')">
    <div class="timestamp">
      <!-- <h4><span>{{formatTime(timeStart)}} - {{formatTime(timeEnd)}}</span></h4> -->
      <h4><span>{{formatTime(timeStart)}}</span></h4>
    </div>
    <div class="separator"></div>
    <div class="timeline-body">
      <div class="header">
        <div v-if="header">
          <h3 class="font-weight-bold">{{header}}</h3>
        </div>
      </div>

      <div class="footer">
        <div class="inline">
          <div v-if="place" class="d-block d-md-inline">
            <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>
            <div v-html="place" class="d-inline"/>
          </div>
          <!-- <div v-if="timeEnd" class="d-inline">
            <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-md-1 ml-md-2"/>
            {{formatTime(timeStart)}} - {{formatTime(timeEnd)}}
          </div> -->
        </div>
        <div v-if="registration">
          <div v-if="submitted">
            <div>{{$t('submitted')}}</div>
          </div>
          <div v-else-if="enableRegistration && registered<maxRegistered">
            <div>{{$t('registrationHasOpened')}}</div>
          </div>
          <div v-else-if="enableRegistration && registered>=maxRegistered">
            <div>{{$t('vilbliventeliste')}}</div>
          </div>
          <div v-else-if="afterRegistration">
            <div>{{$t('registrationClosed')}}</div>
          </div>
          <div v-else>
            <!-- <div>{{$t('registrationOpensAt') + ' ' + formatDate(registrationStart)}}</div> -->
            <div>{{$t('registrationAvailable') + ': ' + formatDate(registrationStart)}}</div>
          </div>
        </div>

        <!-- Shows button for signing up (removed since is is already present in ProgramDescription) -->
        <!-- <div v-if="registration" class='button'>
          <b-button v-if="enableRegistration && !submitted" variant='primary' @click="openDialog">{{$t('register')}}</b-button>
          <b-button v-else disabled variant="dark">{{$t('registrationNotYetAvailable')}}</b-button>
        </div> -->

        <div v-if="isRegistrationOpen">
          <p>{{ registeredText }}</p>
        </div>
      </div>
    </div>
    <!-- <div class="card">
    </div> -->
  </div>
</div>
</template>

<script>
// import { mapMutations } from 'vuex'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMapMarkerAlt, faClock } from '@fortawesome/free-solid-svg-icons'

library.add(faMapMarkerAlt, faClock)
export default {
  name: 'ProgramItem',
  props: [
    'timeStart',
    'timeEnd',
    'place',
    'header',
    'paragraph',
    'registration',
    'maxRegistered',
    'cancelEmail',
    'registrationStart',
    'registrationEnd',
    'name'
  ],
  data () {
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
    isRegistrationOpen () {
      const now = new Date()
      return now >= new Date(this.registrationStart) && now <= new Date(this.registrationEnd)
    },
    registeredText () {
      let filled_spaces = Math.min(this.registered, this.maxRegistered)
      let waiting_list_spaces = Math.max(this.registered - this.maxRegistered, 0)

      let registered_string = `${filled_spaces}/${this.maxRegistered} ${this.$t('registered')}`.toLowerCase()
      if (this.registered >= this.maxRegistered) {
        let waiting_list_string = `${waiting_list_spaces} ${this.$t('onWaitingList')}`.toLowerCase()
        return `${registered_string}, ${waiting_list_string}`
      }
      return registered_string
    },
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
    formatTime (dateObj) {
      let hours = dateObj.getHours()
      let minutes = dateObj.getMinutes()
      hours = (hours > 9) ? String(hours) : ('0' + String(hours))
      minutes = (minutes > 9) ? String(minutes) : ('0' + String(minutes))
      return hours + ':' + minutes  
    },
    formatDate (dateObj) {
      let day = dateObj.getDate()
      let month = dateObj.getMonth() + 1
      let year = dateObj.getFullYear()
      day = (day > 9) ? String(day) : ('0' + String(day))
      month = (month > 9) ? String(month) : ('0' + String(month))
      return this.formatTime(dateObj) + ' ' + day + '.' + month + '.' + year
    },
  }
}
</script>

<style scoped lang="scss">
  .timeline-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    column-gap: 20px;
    align-items: center;
  }
  .separator {
    position: relative;
    width: 6px;
    align-self: stretch;
    background-color: #1d4844;

    /* The circles on the timeline */
    &::after {
      content: '';
      position: absolute;

      // Width and Height of the circle
      width: 25px;
      height: 25px;

      // Move the circle to the center, accounting for its own size
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);

      background-color: white;
      border: 4px solid var(--primary-color);
      border-radius: 50%;
      z-index: 1;
    }
  }
  .timeline-body {
    --line-border-color: rgba(0, 0, 0, 0.125);
    border: 1px solid var(--line-border-color);
    border-radius: 20px;
    border-width: 2px;
    border-color: var(--line-border-color);
    background-color: white;

    // width: 400px;
    padding: 1rem;
    margin: 0.5rem 0; // This ensures there is space between the timeline items, while still allowing the separators to connect
    width: 100%;

    transition-property: border-color, background-color;
    transition-timing-function: ease-in-out;
    transition-duration: 0.1s;
    --primary-color-opacity: #14403c31;
    &:hover {
      border-color: var(--primary-color);
      cursor: pointer;
    }
    .selected-event & {
      border-color: var(--primary-color);
      background-color: var(--primary-color-opacity);
      cursor: default;
    }

    * {
      margin: 0;
    }
  }
  // .numberofpeople {
  //   display: inline;
  // }

  .header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 1em;
    align-items: center;
    // margin-bottom: 20px;
    overflow-wrap: break-word;

    * {
      margin: 0;
    }
    h3 {
      font-size: 1.5em;
    }
    // @media(min-width: 992px) {
    //   flex-direction: row;
    //   margin-bottom: 0;
    // }
  }

  .footer {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 0px;

    // @media(min-width: 992px) {
    //   flex-direction: row;
    //   margin-bottom: 0;
    // }
  }

  .button {
    display: flex;
    flex-direction: row;
    // margin-bottom: 10px;

    // @media(min-width: 768px) {
    //   margin-right: 15px;
    //   flex-direction: row-reverse;
    // }
  }

  .timestamp {
    // outline: 1px solid red;
    // position: absolute;
    // top: calc(50%);
    // left: -20px; // Move left of the timeline
    height: auto;
    white-space: nowrap;
    // transform: translate(-100%, -50%);

    h4 {
        font-size: 1rem;
        opacity: 0.7;
        margin: 0;
    }
  }

  .description {
    font-size:1.1em;
  }

  .modal-content {
    border: none;
    border-radius: 20px;
    background-color: var(--line-border-color);
    color: black;
  }
  .modal-header {
    border-bottom: none;
  }
  .modal-footer {
    border: none;
  }
  .modal-title {
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
      flex-grow: 1;
    }

    .timeline-item::before {
      left: 8px;
      top: 32px;
    }
  }
</style>
