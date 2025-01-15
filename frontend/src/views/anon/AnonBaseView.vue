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
    // min-height: 100vh;
    // width: 95%;
    height: 100%;
    min-width: 320px;
    margin: 0 auto;
    // margin-top: 100px;

    display: flex;
    flex-direction: column;
    gap: 2em;

    h1 {
      font-size: 36px;
      font-weight: 600;
      text-align: center;
      color: black;
      @media(min-width: 768px) {
        text-align: left;
      }
    }

    @media(max-width: 768px) {
      overflow-x: hidden;
    }
    @media(min-width: 480px) {
      // width: 95%;
    }
    @media(min-width: 768px) {
      // width: 95%;
    }
    @media(min-width: 992px) {
      width: 980px;
    }
    @media(min-width: 1200px) {
      width: 1100px;
    }
    // @media(min-width: 1430px) {
    //   width: 1400px;
    // }
  }
</style>
