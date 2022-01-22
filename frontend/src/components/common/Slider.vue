<template>
  <div class="sidemenu">
    <div class="button" v-on:click="menuToggle">
      <div class="burger" v-bind:class="{ visible: menuIsOpen }">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <p v-if="menuIsOpen">Lukk</p>
      <p v-else>Meny</p>
    </div>
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
    <div class="overlay" v-bind:class="{ visible: menuIsOpen }" v-if="menuIsOpen" v-on:click="menuIsOpen = false"></div>
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
        {routeName: 'Listings', linkText: 'Stillingsannonser'},
        {routeName: 'About', linkText: 'Om oss'},
        {routeName: 'Contact', linkText: 'Kontakt'}
      ]
    }
  },
  methods: {
    menuToggle () {
      this.menuIsOpen = !this.menuIsOpen
    }
  }
}
</script>

<style lang="scss" scoped>
  .button {
    cursor: pointer;
    &:hover {
      //filter: brightness(0%) invert(29%) sepia(47%) saturate(587%) hue-rotate(124deg) brightness(94%) contrast(89%);
    }
  }
  p {
    position: absolute;
    color: var(--primary-color);
    margin-left: 30px;
    margin-top: -22px;
    font-size: 18px;
    font-weight: bold;
  }
  span {
    color: var(--background-color-primary);
    border: none;
    text-decoration: none;
  }
  .burger {
    width: 19px;
    color: var(--primary-color);
    height: 15px;
    position: static;
    transform: rotate(0deg);
    transition: .5s ease-in-out;
    cursor: pointer;
    margin-top: 8px;
    margin-right: 60px;
  }
  .burger span {
    display: block;
    position: absolute;
    height: 2px;
    width: 100%;
    background: var(--primary-color);
    opacity: 1;
    left: 0;
    transform: rotate(0deg);
    transition: .25s ease-in-out;
  }
  .burger span:nth-child(1) {
    top: 0px;
    transform-origin: left center;
  }
  .burger span:nth-child(2) {
    top: 5px;
    transform: left center;
  }
  .burger span:nth-child(3) {
    top: 10px;
    transform: left center;
  }
  .burger.visible span:nth-child(1) {
    transform: rotate(45deg);
    top: -2px;
    left: 3px;
  }
  .burger.visible span:nth-child(2) {
    width: 0%;
    opacity: 0;
  }
  .burger.visible span:nth-child(3) {
    transform: rotate(-45deg);
    top: 5px;
  }
  .sidemenu {
    color: var(--background-color-primary);
    border:none;
    outline: 0px;
    @media (min-width: 768px) {
      display:none;
    }
    .slider.visible {
      transform: translate3d(0, 400px, 0);
      transition: all 300ms;
    }
    .slider {
      visibility: hidden;
      position: fixed;
      transition: all 300ms;
      overflow: hidden;
      margin-top: -400px;
      top: 62.5px;
      left: 0;
      width: 100%;
      background: var(--background-color-primary);
      z-index:-1;
      box-shadow: 0px 80px 60px -60px rgba(0,0,0,0.10);
      &.visible {
        visibility: visible;
      }
      hr {
        color: var(--background-color-primary);
        background-color: var(--background-color-primary);
        border-color: var(--background-color-primary);
      }
      ul {
        padding: 0;
        list-style-type: none;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 0px;
        li {
          color: var(--background-color-primary);
          opacity: border 0;
          span {
            opacity: 1;
            border: none;
            color: var(--background-color-primary);
            a {
              color: var(--primary-color);
              opacity: 1;
              font-weight: bold;
              font-size: 16px;
              text-decoration: none;
            }
            a:hover {
              opacity: 1;
            }
          }
        }
      }
    }
    .hamburger {
      display: inline;
    }
  }
  .overlay {
    background-color: var(--background-color-primary);
    width:100%;
    height:100%;
    top:379px;
    left:0;
    position:fixed;
    opacity: 1;
    transition: all 0.5s;
  }
  .overlay.visible {
    opacity: 1;
    transition: all 0.5s;
    -webkit-transition: all 0.5s;
    background-color: rgba(0, 0, 0, 0.02);
  }
</style>
