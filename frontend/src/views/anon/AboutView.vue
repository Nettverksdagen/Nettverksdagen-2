<template>
  <div class="about-view">
    <Content>
      <h1>Om Nettverksdagen</h1>
      <b-row>
        <b-col cols="12" sm="7">
          <p class="introduction">
            Nettverksdagen er en karrieremesse drevet av studenter ved masterstudiet kybernetikk og robotikk ved NTNU.
            Det er et årlig arrangement av studenter fra 3. årstrinn med den hensikt å knytte kontakt mellom studenter og bedrifter innenfor relevante fagområder.
            Arrangementet finner sted i Glassgården i Elektrobygget på Gløshaugen.
            Dette fungerer som fellesområdet til studenter ved linjene Kybernetikk og Robotikk, Energi og Miljø, Elektronisk systemdesign og innovasjon
            og Kommunikasjonsteknologi.
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
