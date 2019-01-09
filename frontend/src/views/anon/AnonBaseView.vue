<template>
  <div class="anon-base">
    <AnonHeader/>
    <Slide width="200" class="sidebar"  @openMenu="handleOpenMenu" @closeMenu="handleCloseMenu" disableEsc>
      <router-link :to="{ name: 'Home' }">Hjem</router-link>
      <router-link :to="{ name: 'Listings' }">Stillinger</router-link>
      <router-link :to="{ name: 'About' }">Om oss</router-link>
      <router-link :to="{ name: 'Contact' }">Kontakt</router-link>
    </Slide>
    <router-view/>
    <AnonFooter/>
    <div class="overlay" v-if="menuIsOpen"></div>
  </div>
</template>

<script>
import AnonHeader from '@/components/anon/AnonHeader.vue'
import AnonFooter from '@/components/anon/AnonFooter.vue'
import { Slide } from 'vue-burger-menu'
export default {
  name: 'AnonBaseView',
  components: {
    AnonHeader,
    AnonFooter,
    Slide
  },
  data () {
    return {
      menuIsOpen: false
    }
  },
  methods: {
    handleOpenMenu: function () {
      this.menuIsOpen = true
    },
    handleCloseMenu: function () {
      this.menuIsOpen = false
    }
  }
}
</script>

<style lang="scss">
  .sidebar {
    @media (min-width: 768px) {
      display:none;
    }
  }
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
  .overlay {
    background: rgba(0, 0, 0, 0.5);
    width:100%;
    height:100%;
    top:0;
    left:0;
    position:fixed;
  }
</style>
