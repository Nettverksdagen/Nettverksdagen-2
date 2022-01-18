<template>
  <div class="about-view">
    <Content>
      <h1>Om Nettverksdagene</h1>
      <b-row>
        <b-col cols="12" lg="6">
          <p class="introduction">
            Nettverksdagene er en karrieremesse arrangert av tredjeårsstudenter på masterstudiet Kybernetikk og robotikk ved NTNU. Målet er å knytte kontakt mellom studenter og bedrifter innenfor relevante fagområder.
            <br>
            <br>
            Inntektene fra Nettverksdagene vil gå til studietur med faglig innhold for studenter ved Kybernetikk og robotikk. Den vil gi en mulighet til å se hvordan nyskapende teknologi brukes i andre land og gi studentene større innsikt i hvordan problemer løses ute i store internasjonale bedrifter. Støtte til Nettverksdagene vil derfor gi uvurderlig kunnskap som vil bidra til å gjøre studentene ekstra verdifulle i fremtiden.
          </p>
        </b-col>
        <b-col cols="12" lg="6" class="d-block d-sm-block">
          <b-img class="image" src="@/assets/excited_people.jpg" fluid alt="Engasjerte studenter i Glassgården"/>
        </b-col>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
export default {
  name: 'AboutView',
  components: {
    Content
  }
}
</script>

<style lang="scss" scoped>
  .introduction {
    font-size:18px;
    text-align: center;
    @media(min-width: 768px) {
      text-align: left;
      margin-right: 30px;
    }
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
  .image {
    border-style: solid;
    border: none;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 20px;
    margin-bottom: 20px;
    @media(min-width: 768px) {
      margin-top: 0px;
    }
  }
  .about-view {
      min-height: 80vh;
  }
</style>
