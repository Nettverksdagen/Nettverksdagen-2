<template>
  <div class="anon-base">
    <AnonHeader/>
    <router-view/>
    <AnonFooter/>
  </div>
</template>

<script>
import AnonHeader from '@/components/anon/AnonHeader.vue'
import AnonFooter from '@/components/anon/AnonFooter.vue'
export default {
  name: 'AnonBaseView',
  components: {
    AnonHeader,
    AnonFooter
  }
}
</script>

<style scoped lang="scss">
</style>
