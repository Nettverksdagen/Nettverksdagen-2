<template>
  <div class="listings">
    <Header/>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import axios from 'axios'
export default {
  components: {
    Header
  },
  data () {
    return {
      info: null
    }
  },
  mounted () {
    axios
      .get('http://127.0.0.1:8000/api/listing/')
      .then(response => (this.info = response))
  },
  name: 'Listings'
}
</script>

<style lang="scss" scoped>
  .listings {
    background-color:#333;
  }
</style>
