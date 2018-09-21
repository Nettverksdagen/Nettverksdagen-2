
<template>
  <div class="home">
    <Header/>
    <img src="@/assets/hero_blur.jpg">
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
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
