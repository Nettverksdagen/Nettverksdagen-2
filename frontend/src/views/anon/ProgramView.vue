<template>
    <Content>
      <div class="program">
        <h1 class="text-center">Program</h1>
        <p class="text-center description mt-3 mb-2">Dette er det foreløpige programmet for Nettverksdagene 2020.</p>
        <h4 class="text-center font-weight-bold"><a href="#stand-map-header">Se standkart her!</a></h4>
        <h3 class="font-weight-bold">30. januar</h3>
        <div class="timeline">
          <div class="timeline-item timeline-item-company">
            <ProgramItem time-start="17:00" time-end="18:00" place="EL3">
              <h4 class="mb-1">Bedriftspresentasjon med Cisco</h4>
            </ProgramItem>
          </div>
        </div>
        <h3 class="font-weight-bold">31. januar</h3>
        <div class="timeline">
          <ProgramItem time-start="10:00">
            <h3 class="font-weight-bold">Nettverksdagen åpner</h3>
            <p class="description">Alle bedriftene står klare i Glassgården kl 10 for å slå av en prat.</p>
          </ProgramItem>
          <ProgramItem time-start="10:00" time-end="11:00" place="H1">
            <h4 class="mb-1">Bedriftspresentasjon med SINTEF</h4>
          </ProgramItem>
        </div>
      </div>
      <h2 id="stand-map-header" class="text-center mb-3">Standkart</h2>
      <img class="stand-map mb-5" src="@/assets/standkart.png">
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
