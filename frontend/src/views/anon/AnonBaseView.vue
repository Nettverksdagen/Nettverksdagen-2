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
  // Define breakpoints for responsive design
  $tiny-width: 300px;
  $small-width: 500px;
  $medium-width: 768px;
  $large-width: 992px;
  $largest-width: 1400px;

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
    min-height: 100vh; /* Necessary to stretch to fill parent */
    // width: 95%;
    height: 100%;
    min-width: 320px;
    margin: 0 auto;
    padding: 0 20px;
    // margin-top: 100px;

    display: flex;
    flex-direction: column;
    gap: 2em;

    // Enforce same font for all page headers
    h1.page-header {
      font-size: 36px;
      font-weight: 600;
      text-align: center;
      color: black;
      text-align: left;
    }

    // @media(max-width: 768px) {
    //   overflow-x: hidden; // What the fuck was this meant to do?
    // }
    @media(min-width: $small-width) {
      width: 95%;
    }
    // @media(min-width: $medium-width) {
    //   width: 95%;
    // }
    @media(min-width: $large-width) {
      width: $large-width;
    }
    // @media(min-width: 1200px) {
    //   width: 1100px;
    // }
    @media(min-width: $largest-width) {
      width: $largest-width;
    }
  }
</style>
