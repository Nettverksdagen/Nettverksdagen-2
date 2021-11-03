<template>
  <div class="sidemenu">
    <font-awesome-icon icon="bars" class="hamburger" v-on:click="menuIsOpen = true"></font-awesome-icon>
    <div class="slider" v-bind:class="{ visible: menuIsOpen }">
      <ul>
        <li v-for="route in routes" :key="route.routeName">
          <span v-on:click="menuIsOpen = false">
            <router-link :to="{ name: route.routeName }">{{ route.linkText }}</router-link>
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
import { faBars, faAdjust, faInfoCircle, faHome } from '@fortawesome/free-solid-svg-icons'
library.add(faBars, faAdjust, faInfoCircle, faHome)
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
        {routeName: 'Program', linkText: 'Program'},
        {routeName: 'Listings', linkText: 'Stillinger'},
        {routeName: 'About', linkText: 'Om oss'},
        {routeName: 'Contact', linkText: 'Kontakt'}
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
  .sidemenu {
    @media (min-width: 1000px) {
      display:none;
    }

    .slider {
      position: fixed;
      right: -200px;
      top: 0;
      width: 150px;
      height:100%;
      transition: 0.5s;
      background: var(--slider-color);
      z-index:200;

      &.visible {
        right: 0;
      }
      ul {
        padding: 0;
        list-style: none;
        li {
          margin: 1em 0;
          span {
            margin: 0 1em;
            a {
              color: var(--text-primary-color);
            }
          }
        }
      }
    }

    .hamburger {
      position:absolute;
      margin: 0 18px 0 0;
      cursor: pointer;
      right: 15px;
      top: 20px;
      width: 30px;
      height: 30px;
      color: var(--header-text-color);
      z-index: 50;
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
