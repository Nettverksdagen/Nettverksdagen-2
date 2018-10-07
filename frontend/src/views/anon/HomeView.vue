<template>
  <div class="home">
    <div class="dude">
      <Hero/>
    </div>
  </div>
</template>

<script>
import Hero from '@/components/anon/Hero.vue'
export default {
  components: {
    Hero
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
