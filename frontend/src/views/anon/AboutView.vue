<template>
  <div class="about-view">
    <Content>
      <h1>Om Nettverksdagene</h1>
      <b-row>
        <b-col cols="12" sm="7">
          <p class="introduction">
            Nettverksdagene er en karrieremesse arrangert av tredjeårsstudenter på masterstudiet Kybernetikk
            og robotikk ved NTNU. Målet er å knytte kontakt mellom studenter og bedrifter innenfor relevante 
            fagområder. Arrangementet 2021 gjennomføres digitalt på plattformen Graduateland onsdag 27. I 
            tillegg gjennomfører vi speed-intervjuer i regi av Poption torsdag 28. 
            <br>
            <br>
            Inntektene fra Nettverksdagene vil gå til studietur med faglig innhold for studenter ved Kybernetikk
            og robotikk. Den vil gi en mulighet til å se hvordan nyskapende teknologi brukes i andre land og gi 
            studentene større innsikt i hvordan problemer løses ute i store internasjonale bedrifter. Støtte til 
            Nettverksdagene vil derfor gi uvurderlig kunnskap som vil gjøre studentene ekstra verdifulle i fremtiden.
          </p>
        </b-col>
        <b-col cols="5" class="d-none d-sm-block">
          <b-img src="@/assets/excited_people.jpg" fluid alt="Engasjerte studenter i Glassgården"/>
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
  }
  .about-view {
      min-height: 80vh;
  }
</style>
