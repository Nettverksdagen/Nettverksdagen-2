<template>
  <div class="anon-base">
    <AnonHeader/>
    <div class="sidebar">
      <font-awesome-icon icon="bars" class="hamburger" v-on:click="menuIsOpen = true"></font-awesome-icon>
      <div class="slider" v-bind:class="{ visible: menuIsOpen }">
        <ul>
          <li><router-link :to="{ name: 'Home' }">Hjem</router-link></li>
          <hr>
          <li><router-link :to="{ name: 'Listings' }">Stillinger</router-link></li>
          <hr>
          <li><router-link :to="{ name: 'About' }">Om oss</router-link></li>
          <hr>
          <li><router-link :to="{ name: 'Contact' }">Kontakt</router-link></li>
          <hr>
          <li><a href="https://nvdagen.no/blogg">Blogg</a></li>
        </ul>
      </div>
    </div>
    <router-view/>
    <AnonFooter/>
    <div class="overlay" v-if="menuIsOpen" v-on:click="menuIsOpen = false"></div>
  </div>
</template>

<script>
import AnonHeader from '@/components/anon/AnonHeader.vue'
import AnonFooter from '@/components/anon/AnonFooter.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faBars } from '@fortawesome/free-solid-svg-icons'
library.add(faBars)
export default {
  name: 'AnonBaseView',
  components: {
    AnonHeader,
    AnonFooter,
    FontAwesomeIcon
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

    .slider {
      position: fixed;
      left: -200px;
      top: 0;
      width: 150px;
      height:100%;
      transition: 0.5s;
      background: #333;
      z-index:200;

      &.visible {
        left: 0;
      }
      ul {
        padding: 0;
        list-style: none;
        li {
          margin: 1em 1em;
          a {
            color: white;
          }
        }
      }
    }

    .hamburger {
      position:absolute;
      left: 15px;
      top: 15px;
      width:20px;
      height:20px;
      color: #333;
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
  .anon-base {
    min-height: 100vh;
  }
</style>
