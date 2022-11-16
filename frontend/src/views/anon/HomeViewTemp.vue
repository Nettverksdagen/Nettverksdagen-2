<template>
  <div class="home">
    <div class="text-center pt-5 card">
      <h3 class="linktext">Vil din bedrift delta på Nettverksdagene 2023?<br>
        <a href="mailto:bedrift@nettverksdagene.no"> Send mail til bedrift@nettverksdagene.no </a>
      </h3>
    </div>
    <div class="dude">
      <!--<Hero/> -->
      <HomeScreenTemp/>
      <businesses></businesses>
      <sponsors></sponsors>
    </div>
  </div>
</template>

<script>
import Hero from '@/components/anon/Hero.vue'
import Businesses from '@/components/anon/Businesses.vue'
import Sponsors from '@/components/anon/Sponsors.vue'
import HomeScreenTemp from '@/components/anon/HomeScreenTemp.vue'
export default {
  components: {
    Hero,
    Businesses,
    Sponsors,
    HomeScreenTemp
  },
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<style lang="scss" scoped>
  .dude {
    width:100%;
  }
  .card {
    width: fit-content;
    margin: auto;
    padding: 2%;
    position: relative;
    border-radius: 20px;
    border-width: 2px;
    border-color: var(--line-border-color);
    background-color: white;
  }

  .linktext {
    color: var(--primary-color);
    font-size: 1rem;
    @media(min-width: 768px) {
      font-size: 32px;
    }
  }
</style>
