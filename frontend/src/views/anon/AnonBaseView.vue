<template>
  <div class="anon-base">
    <AnonHeader/>
    <!-- <Slider/> -->
    <router-view/>
    <AnonFooter/>
  </div>
</template>

<script>
import AnonHeader from '@/components/anon/AnonHeader.vue'
import AnonFooter from '@/components/anon/AnonFooter.vue'
import Slider from '@/components/common/Slider.vue'
export default {
  name: 'AnonBaseView',
  components: {
    AnonHeader,
    AnonFooter,
    Slider
  }
}
</script>

<style lang="scss">
  .bm-burger-button {
    top:16px;
    left:16px;
    width:22px;
    height:20px;
  }
  .bm-item-list {
    a {
      color: #fff;
    }
  }
  .anon-base {
    min-height: 100vh;
  }
</style>
