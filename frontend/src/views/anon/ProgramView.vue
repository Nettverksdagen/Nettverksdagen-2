<template>
  <Content>
    <div class="program">
      <h1 class="text-center">Program</h1>
      <Carousel :perPage="itemsPerPage">
        <Slide class="program-day" :key="'programDay' + index" v-for="(day, index) in program">
          <div class="timeline-child">
            <h3 class="font-weight-bold">{{ formatDate(day[0].timeStart) }}</h3>
            <div class="timeline">
              <div :key="'dayItem' + item.id" v-for="(item) in day">
                <ProgramItem :timeStart="item.timeStart"
                             :header="item.header"
                             :name="item.id"
                             :timeEnd="item.timeEnd"
                             :place="item.place">
                </ProgramItem>
              </div>
            </div>
          </div>
        </Slide>
      </Carousel>
    </div>

  </Content>
</template>

<script>
import Content from '@/components/common/Content.vue'
import ProgramItem from '@/components/anon/ProgramItem.vue'
import {Carousel, Slide} from 'vue-carousel'

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
    Carousel,
    Slide
  },

  data () {
    return {
      itemsPerPage: 3 // Deafault number of days shown
    }
  },

  methods: {
    formatDate (dateObj) {
      let months = ['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'desember']
      let date = dateObj.getDate()
      let month = dateObj.getMonth()
      return String(date) + '. ' + months[month]
    },

    updateItemsPerPage () {
      if (window.innerWidth < 768) {
        this.itemsPerPage = 1
      } else if (window.innerWidth < 1430) {
        this.itemsPerPage = 2
      } else {
        this.itemsPerPage = 3
      }
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
  },

  mounted () {
    this.updateItemsPerPage()
    window.addEventListener('resize', this.updateItemsPerPage)
  },

  beforeDestroy () {
  // Remove the window resize event listener when the component is destroyed
    window.removeEventListener('resize', this.updateItemsPerPage)
  }

}
</script>

<style scoped lang="scss">

.font-weight-bold {
  padding: 1rem;
}
.description {
  font-size: 1.1em;
}

.timeline {
  position: relative;
  margin: 0em 0 3em 6em;
  padding: 1rem 1rem;
  vertical-align: center;
  height: 88%;
}

.timeline-child {
  border: 1px solid rgb(160, 160, 160);
  border-radius: 20px;
  background-color: #f4f4f4;
  padding: 1rem 0rem;
  padding-left: 0px;
  padding-right: 6px;
  margin: 0 8%;
  height: 100%;
}

.timeline::after {
  content: '';
  position: absolute;
  left: -4px;
  width: 6px;
  background-color: #1d4844;
  top: 0;
  bottom: 0;
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
  font-size: 30px;
  font-weight: 60;
  text-align: center;
  color: black;
  margin-bottom: 30px;
  margin-top: 40px;

  @media(min-width: 768px) {
    text-align: left;
  }
}

@media(max-width: 768px) {
  .timeline::after {
    left: -7px;
  }
  
  .timeline {
    padding: 1rem 0rem;
    padding-left: 1rem;
  }

  .timeline-parent::-webkit-scrollbar {
    display: none;
  }

  .program-day {
    width: 100vw;
    min-width: 100vw;
  }

  .timeline-child {
    width: 90%;
    margin-left: auto;
    margin-right: auto;
    max-width: 350px;
    padding-right: 0px;
  }
}
</style>
