<template>
    <Content>
      <div class="program">
        <h1 class="text-center">Program</h1>
        <p class="text-center description mt-3 mb-2">Programmet for Nettverksdagene 2021:</p>
        <!-- <h4 class="text-center font-weight-bold"><a href="#stand-map-header">Se standkart her!</a></h4> -->
        <div :key="'programDay' + index" v-for=" (day , index) in program">
          <h3 class="font-weight-bold">{{formatDate(day[0].timeStart)}}</h3>
          <div class="timeline">
            <div :key="'dayItem' + index" v-for="(item, index) in day">
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
              :name="item.key"
              >
              </ProgramItem>
            </div>
          </div>
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
      let prog = [
        {
          key: 2,
          timeStart: new Date(2021, 0, 26, 18, 15, 0, 0),
          timeEnd: new Date(2021, 0, 26, 19, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Bedriftpresentasjon med Cognite',
          registration: false
        },
        {
          key: 1,
          timeStart: new Date(2021, 0, 25, 15, 0, 0, 0),
          timeEnd: new Date(2021, 0, 27, 15, 0, 0, 0),
          place: 'Poption',
          header: 'Åpent for å bli med på speedintervju i regi av poption!',
          paragraph: ['Studentene kan vise interesse fra og med mandag 25.januar fra kl. 15.00 til og med onsdag 27. kl 15.00. Utvelgelsen av studenter gjør dere fortløpende og innen kl. 17.00 onsdag 27. Invitasjon til aktuelle studenter sendes ut like etterpå. Kandidater blir automatisk booket til et 15 minutters speedintervju over video. Speedintervjuene gjennomføres torsdag 28. kl 09.00 - 16.00. Etter intervjuene er gjennomført kan bedriftene velge om de ønsker å ta studenten med videre i egen rekrutteringsprosess.'],
          registration: false
        },
        {
          key: 3,
          timeStart: new Date(2021, 0, 27, 9, 15, 0, 0),
          timeEnd: new Date(2021, 0, 27, 10, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Morgenbedpress!',
          registration: false
        },
        {
          key: 4,
          timeStart: new Date(2021, 0, 27, 10, 0, 0, 0),
          timeEnd: new Date(2021, 0, 27, 14, 0, 0, 0),
          place: 'nettverksdagene.graduateland.com',
          header: 'Bli med på nettverksdagene via graduateland!',
          registration: false
        },
        {
          key: 5,
          timeStart: new Date(2021, 0, 27, 13, 15, 0, 0),
          timeEnd: new Date(2021, 0, 27, 14, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Bedriftpresentasjon med McKinsey!',
          registration: false
        },
        {
          key: 6,
          timeStart: new Date(2021, 0, 27, 15, 15, 0, 0),
          timeEnd: new Date(2021, 0, 27, 16, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Bedriftpresentasjon med DataRespons!',
          registration: false
        },
        {
          key: 7,
          timeStart: new Date(2021, 0, 27, 17, 15, 0, 0),
          timeEnd: new Date(2021, 0, 27, 18, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Kveldsbedpress!',
          registration: false
        },
        {
          key: 8,
          timeStart: new Date(2021, 0, 28, 9, 15, 0, 0),
          timeEnd: new Date(2021, 0, 28, 10, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Bedriftpresentasjon med DNV GL!',
          registration: false
        },
        {
          key: 9,
          timeStart: new Date(2021, 0, 28, 13, 15, 0, 0),
          timeEnd: new Date(2021, 0, 28, 14, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Bedriftpresentasjon med Galleon!',
          registration: false
        },
        {
          key: 10,
          timeStart: new Date(2021, 0, 28, 17, 15, 0, 0),
          timeEnd: new Date(2021, 0, 28, 18, 15, 0, 0),
          place: 'Digital presentasjon',
          header: 'Surprise bedpress!',
          registration: false
        },
        {
          key: 11,
          timeStart: new Date(2021, 0, 28, 18, 15, 0, 0),
          timeEnd: new Date(2021, 0, 28, 21, 15, 0, 0),
          place: 'Fysisk presentasjon',
          header: 'Bekk inviterer på bedriftspresentasjon med servering!',
          registration: false
        }
      ]

      let sortedProgram = []
      let days = []
      // It now should sort, but maybe uneficiently
      prog.forEach((item, index) => {
        if (index === 0) {
          sortedProgram.push([item])
          days.push(item.timeStart.getDate())
        } else {
          let newSortedProgram = sortedProgram
          let dayExists = false
          let itemInserted = false
          days.forEach((day, index) => {
            if (item.timeStart.getDate() === day) {
              dayExists = true
              let newDayItems = []
              for (let j = 0; j < newSortedProgram[index].length; j++) {
                if (newSortedProgram[index][j].timeStart.getTime() > item.timeStart.getTime() && !itemInserted) {
                  itemInserted = true
                  newDayItems.push(item)
                }
                newDayItems.push(newSortedProgram[index][j])
              }
              if (!itemInserted) {
                newDayItems.push(item)
              }
              newSortedProgram[index] = newDayItems
            }
          })
          if (!dayExists) {
            let newDate = item.timeStart.getDate()
            let inserted = false
            let nextDays = []
            let nextNewSortedProg = []
            for (let i = 0; i < days.length; i++) {
              if (days[i] > newDate && !inserted) {
                inserted = true
                nextDays.push(newDate)
                nextNewSortedProg.push([item])
              }
              nextDays.push(days[i])
              nextNewSortedProg.push(newSortedProgram[i])
            }
            newSortedProgram = nextNewSortedProg
            days = nextDays
            if (!inserted) {
              days.push(newDate)
              newSortedProgram.push([item])
            }
          }
          sortedProgram = newSortedProgram
        }
      })
      /*
      // Testing if it is sorted
      sortedProgram.forEach((day) => {
        day.forEach((item) => {
          console.log(item.key)
        })
      })
      */
      return sortedProgram
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
