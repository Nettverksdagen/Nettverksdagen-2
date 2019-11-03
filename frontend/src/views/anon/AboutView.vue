<template>
  <div class="about-view">
    <Content>
      <h1>Om Nettverksdagene</h1>
      <b-row>
        <b-col cols="12" sm="7">
          <p class="introduction">
            Nettverksdagene er en karrieremesse drevet av studenter ved masterstudiet Kybernetikk og robotikk ved NTNU.
            Det er et årlig arrangement av studenter fra 3. årstrinn med den hensikt å knytte kontakt mellom studenter og bedrifter innenfor relevante fagområder.
            Arrangementet finner sted i Glassgården i Elektrobygget på Gløshaugen.
            Dette fungerer som fellesområdet til studenter ved linjene Kybernetikk og robotikk, Energi og miljø, Elektronisk systemdesign og innovasjon og Kommunikasjonsteknologi.
            <br>
            <br>
            I år har vi valgt å utvide arrangementet til to dager.
            Dette vil gi plass til flere bedrifter, flere studenter vil komme innom og det vil bli en enda større arena hvor bedrifter kan nå ut til studentene.
            <br>
            <br>
            Inntektene fra Nettverksdagene vil gå til en utenlandstur med tungt faglig innhold for studenter ved Kybernetikk og robotikk.
            Den vil gi en mulighet til å se hvordan nyskapende teknologi brukes i andre land og gi studentene større innsikt i hvordan problemer løses ute i store internasjonale bedrifter.
            Støtte til Nettverksdagene vil derfor gi uvurderlig kunnskap som vil gjøre studentene ekstra verdifulle i fremtiden.
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
