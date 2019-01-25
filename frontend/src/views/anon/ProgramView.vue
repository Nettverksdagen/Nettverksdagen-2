<template>
    <Content>
      <div class="program">
        <h1 class="text-center">Program</h1>
        <p class="text-center description mt-3 mb-2">Dette er det foreløpige programmet for Nettverksdagen 2019.</p>
        <h4 class="text-center font-weight-bold"><a href="#stand-map-header">Se standkart her!</a></h4>
        <h3 class="font-weight-bold">30. januar</h3>
        <div class="timeline">
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">13.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med Cisco</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>EL6
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>13.00 - 14.00</p>
              </div>
            </div>
          </div>
        </div>
        <h3 class="font-weight-bold">31. januar</h3>
        <div class="timeline">
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">09.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med BaneNOR</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>H1
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>09.00 - 10.00</p>
              </div>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timestamp">
              <h4><span class="font-weight-bold">10.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h3 class="font-weight-bold">Nettverksdagen åpner</h3>
                <p class="description">Alle bedriftene står klare i Glassgården kl 10 for å slå av en prat.</p>
              </div>
            </div>
          </div>
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">10.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med SINTEF</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>H1
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>10.00 - 11.00</p>
              </div>
            </div>
          </div>
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">11.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med Disruptive Technologies</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>H1
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>11.00 - 12.00</p>
              </div>
            </div>
          </div>
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">12.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med Data Respons</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>EL3
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>12.00 - 13.00</p>
              </div>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timestamp">
              <h4><span class="font-weight-bold">12.05</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h3 class="font-weight-bold">Ballongslipp</h3>
                <p class="description">Møt opp tidlig for å sikre deg noen gode premier. Premiene deles ut kl 14.05.</p>
              </div>
            </div>
          </div>
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">13.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med Mnemonic</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>EL4
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>13.00 - 14.00</p>
              </div>
            </div>
          </div>
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">13.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med Sopra Steria</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>EL3
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>13.00 - 14.00</p>
              </div>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timestamp">
              <h4><span class="font-weight-bold">14.05</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h3 class="font-weight-bold m-0">Premier fra ballongslipp deles ut</h3>
              </div>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timestamp">
              <h4><span class="font-weight-bold">15.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h3 class="font-weight-bold m-0">Nettverksdagen er over</h3>
              </div>
            </div>
          </div>
          <div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">15.00</span></h4>
            </div>
            <div class="card">
              <div class="card-body">
                <h4 class="mb-1">Bedriftspresentasjon med Honeywell</h4>
                <p class="description m-0"><font-awesome-icon :icon="{ prefix: 'fas', iconName: 'map-marker-alt' }" class="mr-1"/>EL6
                  <font-awesome-icon :icon="{ prefix: 'fas', iconName: 'clock' }" class="mr-1 ml-2"/>15.00 - 16.00</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <h2 id="stand-map-header" class="text-center mb-3">Standkart</h2>
      <img class="stand-map mb-5" src="@/assets/standoversikt.png">
    </Content>
</template>

<script>
import Content from '@/components/common/Content.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMapMarkerAlt, faClock } from '@fortawesome/free-solid-svg-icons'
library.add(faMapMarkerAlt, faClock)
export default {
  name: 'ProgramView',
  components: {
    Content
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

  .timeline-item-company::after {
    //background-color: #45b7ae;
  }

  .timestamp {
    position: absolute;
    left: -92px;
    top: 16px;
  }

  /* The actual content */
  .card {
    position: relative;
    border:none;
    border-radius: 0.5em;
    background-color: white;
    box-shadow: 0 1px 2px rgba(0,0,0,0.2), 0 1px 2px rgba(0,0,0,0.15);
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
    .timestamp {
      top: 30px;
      h4 {
        font-size: 1.2em;
      }
    }

    .timeline::after {
      margin-left: -20px;
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
