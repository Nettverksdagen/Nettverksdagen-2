<template>
  <div class="program">
    <Content>
      <h1>Program</h1>
      <p>Nettverksdagen finner sted 31. januar 2019 i Elbygget på NTNU.</p>
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
</style>
