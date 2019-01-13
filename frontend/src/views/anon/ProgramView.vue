<template>
  <div class="program">
    <Content>
      <b-row>
        <b-col cols="12" md="6">
          <h1>Program</h1>
          <p>Dette er det foreløpige programmet for Nettverksdagen 2019. Mer informasjon kommer her etter hvert. Stay tuned!</p>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <hr>
          <div class="program-element">
            <h2 class="time-header"><span class="font-weight-bold">10.00</span> – Nettverksdagen åpner</h2>
            <p class="description">Alle bedriftene står klare i Glassgården kl 10 for å slå av en prat.</p>
          </div>

          <hr>
          <div class="program-element">
            <h2 class="time-header"><span class="font-weight-bold">12.05</span> – Ballongslipp</h2>
            <p class="description">Møt opp tidlig for å sikre deg noen gode premier. Premiene deles ut kl 14.05.</p>
          </div>

          <hr>
          <div class="program-element">
            <h2 class="time-header"><span class="font-weight-bold">14.05</span> – Premier fra ballongslippet deles ut</h2>
          </div>

          <hr>
          <div class="program-element">
            <h2 class="time-header"><span class="font-weight-bold">15.00</span> – Nettverksdagen er over</h2>
          </div>
          <hr>
        </b-col>
        <b-col cols="6" class="d-none d-md-block">
          <div class="stand-map-placeholder">
            <h5 class="text-center">Standkart kommer her</h5>
          </div>
        </b-col>
      </b-row>
    </Content>
  </div>
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
  .program-element {
    margin: 2em 0;
  }
  .description {
    font-size:1.3em;
  }
  .stand-map-placeholder {
    height: calc(100% - 2em);
    width: 100%;
    background: #d5dcdb;
    border-radius: 5px;
    margin: 1em 0;
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
</style>
