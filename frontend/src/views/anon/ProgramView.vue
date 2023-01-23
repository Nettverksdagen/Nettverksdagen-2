<template>
    <Content>
      <div class="program">
        <h1 class="text-center">Program</h1>
        <!-- <p class="text-center description mt-3 mb-2">{{$t('program22')}}</p> -->
        <!-- <h4 class="text-center font-weight-bold"><a href="#stand-map-header">Se standkart her!</a></h4> -->
        <div :key="'programDay' + index" v-for="(day, index) in program">
          <h3 class="font-weight-bold">{{formatDate(day[0].timeStart)}}</h3>
          <div class="timeline">
            <div :key="'dayItem' + item.id" v-for="(item) in day">
              <ProgramItem
              :timeStart="item.timeStart"
              :timeEnd="item.timeEnd"
              :place="item.place"
              :header="item.header"
              :paragraph="item.paragraph"
              :registration="item.registration"
              :maxRegistered="item.maxRegistered"
              :registered="item.registered"
              :cancelEmail="item.cancelEmail"
              :registrationStart="item.registrationStart"
              :registrationEnd="item.registrationEnd"
              :name="item.id"
              >
              </ProgramItem>
            </div>
          </div>
        </div>
        <div id="bankett">
        </div>
      </div>

      <!-- Uncomment this to get the stand maps from 2020 at the bottom. Disabled for 2021 since it was held digitally.
      <h2 id="stand-map-header" class="text-center mb-3">Standkart</h2>
      <h3 class="text-center mb-3">29. januar</h3>
      <img class="stand-map mb-5" src="@/assets/standkart-dag1.png">
      <h3 class="text-center mb-3">30. januar</h3>
      <img class="stand-map mb-5" src="@/assets/standkart-dag2.png">
      -->

    </Content>
</template>

<script>
import Content from '@/components/common/Content.vue'
import ProgramItem from '@/components/anon/ProgramItem.vue'

function isSameDay (lhs, rhs) {
  return (
    lhs.getFullYear() === rhs.getFullYear() &&
    lhs.getMonth() === rhs.getMonth() &&
    lhs.getDate() === rhs.getDate()
  )
}

export default {
  name: 'ProgramView',
  components: {
    Content,
    ProgramItem
  },
  methods: {
    formatDate (dateObj) {
      let months = ['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'desember']
      let date = dateObj.getDate()
      let month = dateObj.getMonth()
      return String(date) + '. ' + months[month]
    }
  },
  computed: {
    program: function () {
      let prog = this.$store.getters['program/anonProgram']

      // Sort the program by start time
      let sortedProg = [...prog].sort((lhs, rhs) => {
        return lhs.timeStart - rhs.timeStart
      })

      let days = [[sortedProg.at(0)]]
      sortedProg.slice(1).forEach((item) => {
        let lastItem = days.at(-1).at(-1)
        if (isSameDay(item.timeStart, lastItem.timeStart)) {
          // This program item has the same start date as the last one, so we
          // add the item to the current day
          days.at(-1).push(item)
        } else {
          // This program item has a different start date from the last one, so
          // we add a new day to the program containing this item
          days.push([item])
        }
      })

      return days
    }
  }
}
</script>

<style scoped lang="scss">
  .description {
    font-size:1.1em;
  }
  .stand-map {
    height: calc(100% - 2em);
    background: #dee2e2;
    border-radius: 8px;
    padding: 3em 1em;
    width: 100%;
    box-shadow: 0 1px 2px rgba(0,0,0,0.2), 0 1px 2px rgba(0,0,0,0.15);

    @media(min-width: 576px) {
      padding: 3em 1em;
    }

    @media(min-width: 768px) {
      padding: 3em 4em;
    }

    @media(min-width: 966px) {
      padding: 4em 14em;
    }
  }
  .timeline {
    position: relative;
    margin: 1em 0 3em 6em;
  }
  .timeline::after {
    content: '';
    position: absolute;
    width: 6px;
    background-color: #1d4844;
    top: 0;
    bottom: 0;
    margin-left: -3px;
  }

  .btn-primary {
    background-color: #1d4844;
    color: white !important;
    border-radius: 25px;
    border: none;
    padding: 10px 20px;
  }

  .img-company {
    height: 2rem;
    max-width: 100%;
    margin-right: 1rem;
  }

  h1 {
    font-size: 36px;
    font-weight: 600;
    text-align: center;
    color: black;
    margin-bottom: 30px;
    margin-top: 40px;
    @media(min-width: 768px) {
      text-align: left;
    }
  }

  @media(max-width: 966px) {
    h3 {
      font-size: 1.3em;
    }
    h4 {
      font-size: 1.2em;

    }
  }

  @media(max-width: 768px) {
    .timeline::after {
      margin-left: -20px;
    }
  }

</style>
