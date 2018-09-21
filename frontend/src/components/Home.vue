
<template>
  <div class="home">
    <Header/>
    <img class="hero" src="@/assets/hero_blur.jpg">
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
export default {
  components: {
    Header
  },
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .hero {
    width:100%;
  }
</style>
