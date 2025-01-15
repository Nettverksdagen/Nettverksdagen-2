<template>
  <Content>
    <div class="program">
      <h1 class="text-center">Program</h1>
      <div class="days-list">
        <button
          v-for="(day, index) in program"
          :key="'dayButton' + index"
          @click="selectDay(index)"
          :class="{ 'selected-day': selectedDayIndex === index }"
        >
          {{ formatDate(day[0].timeStart) }}
        </button>
      </div>
      <div v-if="selectedDay" class="program-wrapper">
        <div class="timeline">
          <div
            :key="'dayItem' + item.id"
            v-for="(item) in selectedDay"
            @click="selectProgramItem(item)"
            :class="{ 'selected-event': selectedProgramItem && selectedProgramItem.id === item.id }"
          >
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
            <div v-if="isMobile && selectedProgramItem && selectedProgramItem.id === item.id">
              <ProgramDescription
                :timeStart="selectedProgramItem.timeStart"
                :timeEnd="selectedProgramItem.timeEnd"
                :place="selectedProgramItem.place"
                :header="selectedProgramItem.header"
                :paragraph="selectedProgramItem.paragraph"
                :registration="selectedProgramItem.registration"
                :maxRegistered="selectedProgramItem.maxRegistered"
                :registered="selectedProgramItem.registered"
                :cancelEmail="selectedProgramItem.cancelEmail"
                :registrationStart="selectedProgramItem.registrationStart"
                :registrationEnd="selectedProgramItem.registrationEnd"
                :name="selectedProgramItem.id"
              >
              </ProgramDescription>
            </div>
          </div>
        </div>
        <!-- <div> -->
          <ProgramDescription  v-if="!isMobile && selectedProgramItem"
            :timeStart="selectedProgramItem.timeStart"
            :timeEnd="selectedProgramItem.timeEnd"
            :place="selectedProgramItem.place"
            :header="selectedProgramItem.header"
            :paragraph="selectedProgramItem.paragraph"
            :registration="selectedProgramItem.registration"
            :maxRegistered="selectedProgramItem.maxRegistered"
            :registered="selectedProgramItem.registered"
            :cancelEmail="selectedProgramItem.cancelEmail"
            :registrationStart="selectedProgramItem.registrationStart"
            :registrationEnd="selectedProgramItem.registrationEnd"
            :name="selectedProgramItem.id"
          >
          </ProgramDescription>
        <!-- </div> -->
      </div>
      <div id="bankett"></div>
    </div>
  </Content>
</template>

<script>
import Content from '@/components/common/Content.vue'
import ProgramItem from '@/components/anon/ProgramItem.vue'
import ProgramDescription from '@/components/anon/ProgramDescription.vue'

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
    ProgramItem,
    ProgramDescription
  },
  data () {
    return {
      selectedProgramItem: null,
      selectedDayIndex: 0,
      isMobile: window.innerWidth <= 768
    }
  },
  mounted () {
    window.addEventListener('resize', this.handleResize)
    if (this.program.length > 0 && this.program[0].length > 0) {
      this.selectedProgramItem = this.program[0][0]
    }
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.handleResize)
  },
  watch: {
    program (newProgram) {
      if (newProgram.length > 0 && newProgram[0].length > 0) {
        this.selectedProgramItem = newProgram[0][0]
      }
    }
  },
  methods: {
    formatDate (dateObj) {
      let months = ['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'desember']
      let date = dateObj.getDate()
      let month = dateObj.getMonth()
      return String(date) + '. ' + months[month]
    },
    selectProgramItem (item) {
      this.selectedProgramItem = item
    },
    selectDay (index) {
      this.selectedDayIndex = index
      this.selectedProgramItem = this.program[index][0]
    },
    handleResize () {
      this.isMobile = window.innerWidth <= 768
    }
  },
  computed: {
    program: function () {
      let prog = this.$store.getters['program/anonProgram']

      // Sort the program by start time and end time
      let sortedProg = [...prog].sort((lhs, rhs) => {
        // Sort by end times
        return lhs.timeEnd - rhs.timeEnd
      }).sort((lhs, rhs) => {
        // Sort by start times, since stable sort the end times will be preserved
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
    },
    selectedDay () {
      return this.program[this.selectedDayIndex]
    }
  }
}
</script>

<style scoped lang="scss">
  .description {
    font-size:1.1em;
  }
  // .stand-map {
  //   height: calc(100% - 2em);
  //   background: #dee2e2;
  //   border-radius: 8px;
  //   padding: 3em 1em;
  //   width: 100%;
  //   box-shadow: 0 1px 2px rgba(0,0,0,0.2), 0 1px 2px rgba(0,0,0,0.15);

  //   @media(min-width: 576px) {
  //     padding: 3em 1em;
  //   }

  //   @media(min-width: 768px) {
  //     padding: 3em 4em;
  //   }

  //   @media(min-width: 966px) {
  //     padding: 4em 14em;
  //   }
  // }
  .program {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 1em;
    padding: 0.5em;

    h1 {
      margin-bottom: 0;
    }
  }
  .program-wrapper {
    display: flex;
    flex-direction: row;
    // justify-content: space-between;
    gap: 2em;
    // align-items: stretch;
    // margin-bottom: 2em;
    // @media(max-width: 768px) {
    //   flex-direction: column;
    // }
  }
  .timeline {
    flex: 1;

    // @media (min-width: 768px) {
    //   position: sticky;
    //   top: 4em;
    //   overflow: scroll;
    //   scroll-behavior: contain;
    //   max-height: 100vh;
    // }
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

  // .selected-event {
  //   background-color: #e0f7fa;
  // }

  .days-list {
    display: flex;
    justify-content: center;
    // margin-bottom: 20px;
    button {
      margin: 0 10px;
      padding: 10px 20px;
      border: none;
      background-color: #f0f0f0;
      cursor: pointer;
      &.selected-day {
        background-color: #1d4844;
        color: white;
      }
    }
  }
</style>
