<template>
    <Content>
      <div class="program">
        <h1 class="text-center">Program</h1>
        <p class="text-center description mt-3 mb-2">Dette er det foreløpige programmet for Nettverksdagen 2019. Mer informasjon kommer her etter hvert.</p>
        <p class="text-center description"><a href="">Se standkart her!</a></p>
        <div class="timeline">
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
          <!--<div class="timeline-item timeline-item-company">
            <div class="timestamp">
              <h4><span class="font-weight-bold">12.05</span></h4>
            </div>
            <div class="card">
              <div class="card-body d-flex">
                <div>
                  <b-img class="img-company" src="@/assets/kjeldsberg.png"></b-img>
                </div>
                <div class="ml-md-3 d-flex justify-content-center flex-column">
                  <h3 class="font-weight-bold m-0">Bedriftspresentasjon med Kjeldsberg Kaffe</h3>
                </div>
              </div>
            </div>
          </div>-->
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
        </div>
      </div>
      <div class="stand-map-placeholder">
        <h5 class="text-center">Standkart kommer her</h5>
      </div>
    </Content>
</template>

<script>
import Content from '@/components/common/Content.vue'
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
  .stand-map-placeholder {
    height: calc(100% - 2em);
    background: #c3c9c8;
    border-radius: 8px;
    padding: 4em;
    h5 {
      color: #122e2c;
      font-size:2em;
      text-align: center;
      font-weight: bold;
      position:relative;
      top: calc(50% - 0.5em);

      @media(max-width: 966px) {
        font-size:1.5em;
      }
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
    background-color: #45b7ae;
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
    height: 6rem;
    max-width: 100%;
  }

  @media(max-width: 966px) {
    h3 {
      font-size: 1.3em;
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
