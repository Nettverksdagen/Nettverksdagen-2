<template>
  <div class="home">
    <div class="text-center pt-5">
      <h3>Vil din bedrift delta på Nettverksdagene 2023?</h3>
      <h3><a href="mailto:bedrift@nettverksdagene.no"> Send mail til bedrift@nettverksdagene.no </a></h3>
    </div>
    <div class="dude">
      <!--<Hero/> -->
      <HomeScreenTemp/>
    </div>
  </div>
</template>

<script>
import Hero from '@/components/anon/Hero.vue'
import HomeScreenTemp from '@/components/anon/HomeScreenTemp.vue'
export default {
  components: {
    Hero,
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
</style>
