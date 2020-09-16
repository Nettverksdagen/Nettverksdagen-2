<template>
    <Content>
      <div class="program">
        <h1 class="text-center">Program</h1>
        <p class="text-center description mt-3 mb-2">Dette var programmet for Nettverksdagene 2020.</p>
        <h4 class="text-center font-weight-bold"><a href="#stand-map-header">Se standkart her!</a></h4>
        <div v-for="(day, index) in program">
          <h3 class="font-weight-bold">{{formatDate(day[0].timeStart)}}</h3>
          <div class="timeline">
            <div v-for="(item, index) in day" >
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
              >
              </ProgramItem>
            </div>
          </div>
        </div>
      </div>
      <h2 id="stand-map-header" class="text-center mb-3">Standkart</h2>
      <h3 class="text-center mb-3">29. januar</h3>
      <img class="stand-map mb-5" src="@/assets/standkart-dag1.png">
      <h3 class="text-center mb-3">30. januar</h3>
      <img class="stand-map mb-5" src="@/assets/standkart-dag2.png">
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
    formatDate(dateObj){
      let months = ["januar"]
      let date = dateObj.getDate();
      let month = dateObj.getMonth();
      return String(date) + ". " + months[month]
    }
  },
  computed: {
    program: function(){
      let prog = [
        {
          key: 3,
          timeStart: new Date(2021, 0, 29, 10, 0, 0,0),
          place:'Glassgården, Elektrobygget', 
          header: 'Standområdet åpner!',
        },
        
        {
          key: 4,
          timeStart: new Date(2021, 0, 29, 12, 10, 0,0),
          place:'Glassgården, Elektrobygget', 
          header: 'Ballongslipp!',
        },
        {
          key: 8,
          timeStart: new Date(2021, 0, 29, 17, 15, 0,0), 
          place:'EL1, Gamle Elektro', 
          header: 'Bedriftpresentasjon med Bekk',
          paragraph: ['Med bespisning på Olivia Solsiden', 'Dette arrangementet er fullt.'],
        },
         {
          key: 1,
          timeStart: new Date(2021, 0, 28, 17, 30, 0,0),
          place:'EL1, Gamle Elektro', 
          header: 'Bedriftpresentasjon med Honeywell',
          paragraph: ['Med bespisning på Graffi Grill.', 'Dette arrangementet er fullt.'],
          registration: true,
          maxRegistered: 10,
          registered: 5,
          cancelEmail: "kska@stud.ntnu.no",
          registrationStart: new Date(2020, 8, 16, 18, 58, 0,0),
        },
      
       {
          key: 6,
          timeStart: new Date(2021, 0, 29, 14, 0, 0,0),
          place:'Glassgården, Elektrobygget', 
          header: 'Premieutdeling!',
        },
        {
          key: 7,
          timeStart: new Date(2021, 0, 29, 14, 15, 0,0),
          timeEnd: new Date(2021, 0, 29, 15, 0, 0,0), 
          place:'EL1, Gamle Elektro', 
          header: 'Bedriftpresentasjon med Imatis',
          paragraph: ['Med servering av baguetter og mineralvann.', 'Påmeldingen er avsluttet.']
        },
        
          {
          key: 5,
          timeStart: new Date(2021, 0, 29, 12, 15, 0,0),
          timeEnd: new Date(2021, 0, 29, 13, 0, 0,0), 
          place:'KJL1, Kjelhuset', 
          header: 'Prosjektpresentasjon med Data Respons R&D Services',
          paragraph: ['Bli med på Kahootkonkurranse og vinn AirPods Pro.', 'Påmeldingen er avsluttet.']
        },
        {
          key: 9,
          timeStart: new Date(2021, 0, 30, 9, 15, 0,0),
          timeEnd: new Date(2021, 0, 30, 10, 15, 0,0), 
          place:'EL5, Gamle Elektro', 
          header: 'Frokostpresentasjon med National Oilwell Varco',
          paragraph: ['Med servering av baguetter og kaffe.', 'Påmeldingen er avsluttet.']
        },
        
        {
          key: 2,
          timeStart: new Date(2021, 0, 29, 9, 15, 0,0),
          timeEnd: new Date(2021, 0, 29, 10, 15, 0,0), 
          place:'EL6, Gamle Elektro', 
          header: 'Frokostpresentasjon med Sopra Steria',
          paragraph: ['Med servering av baguetter og kaffe.', 'Påmeldingen er avsluttet.']
        },
        {
          key: 11,
          timeStart: new Date(2021, 0, 30, 11, 15, 0,0),
          timeEnd: new Date(2021, 0, 30, 12, 0, 0,0), 
          place:'S8, Stripa (Sentralbygg 2)', 
          header: 'Lønsjpresentasjon med Maritime Robotics',
          paragraph: ['Med servering av baguetter og mineralvann.', 'Påmeldingen er avsluttet.']
        },
        {
          key: 12,
          timeStart: new Date(2021, 0, 30, 12, 10, 0,0),
          place:'Glassgården, Elektrobygget', 
          header: 'Ballongslipp!',
        },
        {
          key: 13,
          timeStart: new Date(2021, 0, 30, 12, 15, 0,0),
          timeEnd: new Date(2021, 0, 30, 13, 0, 0,0), 
          place:'S1, Stripa (Sentralbygg 1)', 
          header: 'Prosjektpresentasjon med Data Respons R&D Services',
          paragraph: ['Bli med på Kahootkonkurranse og vinn AirPods Pro.', 'Påmeldingen er avsluttet.']
        },
        {
          key: 10,
          timeStart: new Date(2021, 0, 30, 10, 0, 0,0),
          place:'Glassgården, Elektrobygget', 
          header: 'Standområdet åpner',
          paragraph: ['Goodiebags til de 50 første som kommer innom!']
        },
        {
          key: 14,
          timeStart: new Date(2021, 0, 30, 14, 0, 0,0),
          place:'Glassgården, Elektrobygget', 
          header: 'Premieutdeling!',
        },
         {
          key: 15,
          timeStart: new Date(2021, 0, 30, 14, 15, 0,0),
          timeEnd: new Date(2021, 0, 30, 15, 30, 0,0), 
          place:'EL6, Gamle Elektro', 
          header: 'Kryptografi-skattejakt med DNB',
          paragraph: ['Med servering av baguetter og mineralvann. Premie til vinnerne!', 'Påmeldingen er avsluttet.']
        },        
      ];
      let sortedProgram = [];
      let days = [];
      // It now should sort, but maybe uneficiently
      prog.forEach((item, index) => {
        if(index===0){
          sortedProgram.push([item]);
          days.push(item.timeStart.getDate());
        }else{
          let newSortedProgram = sortedProgram;
          let dayExists = false;
          let itemInserted = false;
            days.forEach((day, index) => {
              if(item.timeStart.getDate() == day){
                dayExists = true
                let newDayItems = [];
                for(let j=0; j<newSortedProgram[index].length; j++){
                  if(newSortedProgram[index][j].timeStart.getTime()>item.timeStart.getTime() && !itemInserted){
                    itemInserted=true;
                    newDayItems.push(item);
                  }
                    newDayItems.push(newSortedProgram[index][j])
                  
                }
                if(!itemInserted){
                  newDayItems.push(item);
                }
                newSortedProgram[index] = newDayItems;
              }
            })
          if(!dayExists){
            let newDate = item.timeStart.getDate();
            let inserted = false;
            let nextDays = [];
            let nextNewSortedProg = [];
            for( let i = 0; i<days.length; i++){
              if(days[i]>newDate && !inserted){
                inserted=true;
                nextDays.push(newDate);
                nextNewSortedProg.push([item]);
              }
                nextDays.push(days[i]);
                nextNewSortedProg.push(newSortedProgram[i]);
              
            }
            newSortedProgram = nextNewSortedProg;
            days = nextDays;
            if(!inserted){
              days.push(newDate);
              newSortedProgram.push([item]);
            }
          }
          sortedProgram = newSortedProgram;
        }
      })

      /*
      // Testing if it is sorted
      sortedProgram.forEach((day) => {
        day.forEach((item) => {
          console.log(item.key);
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
