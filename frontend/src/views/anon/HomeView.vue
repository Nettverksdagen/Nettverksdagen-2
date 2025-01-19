<template>
  <div class="home">
    <!-- <div class="text-center pt-5">
      <h3>{{$t('doyour')}}</h3>
      <h3><a href="mailto:bedrift@nettverksdagene.no">{{$t('sendmailto') + ' bedrift@nettverksdagene.no' }}</a></h3>
    </div> -->
    <HomeScreen/>
    <StandMap/>
    <businesses></businesses>
    <sponsors></sponsors>
  </div>
</template>

<script>
import Businesses from '@/components/anon/Businesses.vue'
import Sponsors from '@/components/anon/Sponsors.vue'
import HomeScreen from '@/components/anon/HomeScreen.vue'
import StandMap from '@/components/anon/StandMap.vue'
export default {
  components: {
    Businesses,
    Sponsors,
    HomeScreen,
    StandMap
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
  .home {
    display: flex;
    flex-direction: column;
    gap: 5em; // Very simple way to add spacing between elements (like splash screen and map)
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
