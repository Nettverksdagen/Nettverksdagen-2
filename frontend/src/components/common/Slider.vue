<template>
  <div class="sidebar">
    <font-awesome-icon icon="bars" class="hamburger" v-on:click="menuIsOpen = true"></font-awesome-icon>
    <div class="slider" v-bind:class="{ visible: menuIsOpen }">
      <ul>
        <li v-for="route in routes" :key="route.routeName">
          <span v-on:click="menuIsOpen = false">
            <router-link :to="{ name: route.routeName }">{{ route.linkText }}</router-link>
          </span>
          <hr>
        </li>
        <li>
          <span v-on:click="menuIsOpen = false">
            <a href="https://nvdagen.no/blogg">Blogg</a>
          </span>
          <hr>
        </li>
      </ul>
    </div>
    <div class="overlay" v-if="menuIsOpen" v-on:click="menuIsOpen = false"></div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faBars } from '@fortawesome/free-solid-svg-icons'
library.add(faBars)
export default {
  name: 'Slider',
  components: {
    FontAwesomeIcon
  },
  data () {
    return {
      menuIsOpen: false,
      routes: [
        {routeName: 'Home', linkText: 'Hjem'},
        {routeName: 'Listings', linkText: 'Stillinger'},
        {routeName: 'About', linkText: 'Om oss'},
        {routeName: 'Contact', linkText: 'Kontakt'}
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
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
          margin: 1em 0;
          span {
            margin: 0 1em;
            a {
              color: white;
            }
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
  .overlay {
    background: rgba(0, 0, 0, 0.5);
    width:100%;
    height:100%;
    top:0;
    left:0;
    position:fixed;
    z-index:100;
  }
</style>
