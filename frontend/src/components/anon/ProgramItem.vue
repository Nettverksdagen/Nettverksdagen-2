<template>
  <div class="timeline-item">
    <div class="timestamp">
      <h4><span class="font-weight-bold">{{formatTime(timeStart)}}</span></h4>
    </div>
    <div class="card">
      <div class="card-body">
        <div class="header">
          <div v-if="header">
            <h3 class="font-weight-bold">{{header}}</h3>
          </div>
          <div v-if="registration && maxRegistered">
            <h5>{{registered + '/' + maxRegistered + ' påmeldte'}}</h5>
          </div>
        </div>
        <div v-if="paragraph">
          <div v-for="line in paragraph" >
            <p class="description">{{line}}</p>
          </div>
        </div>
        <div v-if="registration" class="button">
          <button v-if="enableRegistration" type="button" class="btn btn-primary">Påmelding</button>
          <button v-else type="button" class="btn btn-primary disabled">Påmelding</button>
        </div>
        <div class="footer">
          <div class="inline">
            <div v-if="place" class="d-inline">
              <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>
              {{place}}
            </div>
            <div v-if="timeEnd" class="d-inline">
              <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>
              {{formatTime(timeStart)}} - {{formatTime(timeEnd)}}
            </div>
          </div>
          <div v-if="registration && cancelEmail">
              <b-link :href="'mailto:' + cancelEmail">{{'Ønsker du å melde deg av klikk her'}}</b-link>
          </div>
          <div v-if="registration">
              <div v-if="enableRegistration">
                <div>Påmelding har beggynt</div>
              </div>
              <div v-else-if="afterRegistration">
                <div>Påmelding er ferdig</div>
              </div>
              <div v-else>
              <div>{{'Påmelding begynner ' + formatDate(registrationStart)}}</div>
              </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMapMarkerAlt, faClock } from '@fortawesome/free-solid-svg-icons'
library.add(faMapMarkerAlt, faClock)
export default {
  name: 'ProgramItem',
  props: ['timeStart','timeEnd', 'place', 'header', 'paragraph', 'registration', 'maxRegistered', 'registered', 'cancelEmail', 'registrationStart', 'registrationEnd'],
  computed: {
    beforeRegistration: function(){
      let now = new Date();
      return this.$props.registrationStart.getTime()>now.getTime();
    },
    afterRegistration: function(){
      let now = new Date();
      if(this.$props.registrationEnd){
        return this.$props.registrationEnd.getTime()<now.getTime();
      }
      return this.$props.timeStart.getTime()<now.getTime()
    },
    enableRegistration: function(){
      if(!this.$props.registration){
        return false;
      }
      if(this.beforeRegistration){
        return false
      }
      if(this.afterRegistration){
        return false
      }
      return true;
    }
  },
  methods: {
    formatTime(dateObj){
      let hours = dateObj.getHours();
      let minutes = dateObj.getMinutes();
      hours = (hours>9) ? String(hours) : ('0' + String(hours));
      minutes = (minutes>9) ? String(minutes) : ('0' + String(minutes));
      return hours + ':' + minutes
    },
    formatDate(dateObj){
      let day = dateObj.getDate();
      let month = dateObj.getMonth() + 1;
      let year = dateObj.getFullYear();
      day = (day>9) ? String(day) : ('0' + String(day));
      month = (month>9) ? String(month) : ('0' + String(month));
      return this.formatTime(dateObj) +' '+ day + '.' +month+'.'+year
    }
  }
}
</script>

<style scoped lang="scss">
  .card {
    position: relative;
    border:none;
    border-radius: 0.5em;
    background-color: white;
    box-shadow: 0 1px 2px rgba(0,0,0,0.2), 0 1px 2px rgba(0,0,0,0.15);
  }

  .timeline-item {
    padding: 15px 0 15px 40px;
    position: relative;
    background-color: inherit;
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
    border: medium solid white;
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
    border: 4px solid #1d4844;
    top: 18px;
    border-radius: 50%;
    z-index: 1;
    left: -13px;
  }

  .header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .footer {
     display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .button {
    margin-right: 15px;
    display: flex;
    flex-direction: row-reverse
  }


  .timestamp {
    position: absolute;
    left: -92px;
    top: 16px;
  }

  .description {
    font-size:1.1em;
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
