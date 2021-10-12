<template>
  <div class="home">
    <div class="dude">
      <Hero/>
    </div>
    <div class="text-center pt-5">
      <h3>Vil din bedrift delta på Nettverksdagene 2022?</h3>
      <h3><a href="mailto:bedrift@nettverksdagene.no">Meld interesse her</a>.</h3>
    </div>
    <businesses></businesses>
    <sponsors></sponsors>
  </div>
</template>

<script>
import Hero from '@/components/anon/Hero.vue'
import Businesses from '@/components/anon/Businesses.vue'
import Sponsors from '@/components/anon/Sponsors.vue'
export default {
  components: {
    Hero,
    Businesses,
    Sponsors
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
</style>
