<template>
  <div class="hero-hex-box">
    <div class="wrapper">
      <div class="hero-hex-wrapper">
        <HeroHex :hex-icon="hexIcon" :hex-icon-alt="hexTitle"/>
      </div>
      <h3 class="hero-hex-title">{{ hexTitle }}</h3>
      <span><slot></slot></span>
    </div>
  </div>
</template>

<script>
import HeroHex from '@/components/anon/HeroHex.vue'
export default {
  props: ['hexIcon', 'hexTitle'],
  components: {
    HeroHex
  }
}
</script>

<style lang="scss" scoped>
  .hero-hex-box {
    width:250px;
    @media(min-width: 992px) {
      width:300px;
    }
    color:#194743;
    //text-shadow: 0 1px 2px rgba(0,0,0,0.7);
    text-align:center;
  }

  .hero-hex-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: center;
  }

  .hero-hex-title {
    @media(max-width: 992px) {
      font-size:25px;
    }
  }
</style>
