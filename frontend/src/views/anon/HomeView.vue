<template>
  <div class="home">
    <div class="text-center pt-5">
      <h3>{{$t('doyour')}}</h3>
      <h3><a href="mailto:bedrift@nettverksdagene.no">{{$t('sendmailto') + ' bedrift@nettverksdagene.no' }}</a></h3>
    </div>
    <div class="dude">
      <!--<Hero/> -->
      <HomeScreen/>
    </div>
    <businesses></businesses>
    <sponsors></sponsors>
  </div>
</template>

<script>
import Hero from '@/components/anon/Hero.vue'
import Businesses from '@/components/anon/Businesses.vue'
import Sponsors from '@/components/anon/Sponsors.vue'
import HomeScreen from '@/components/anon/HomeScreen.vue'
export default {
  components: {
    Hero,
    Businesses,
    Sponsors,
    HomeScreen
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
</style>
