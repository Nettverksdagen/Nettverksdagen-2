<template>
  <div class="home">
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
    position: relative;
    border-radius: 20px;
    border-width: 2px;
    border-color: var(--line-border-color);
    background-color: white;
  }
</style>
