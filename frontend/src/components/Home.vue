
<template>
  <div class="home">
    <Header/>
    <div class="dude">
      <Hero/>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Hero from '@/components/Hero.vue'
export default {
  components: {
    Header,
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
