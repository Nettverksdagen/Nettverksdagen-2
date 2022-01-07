<template>
  <div class="sidemenu">
    <div class="button" v-on:click="menuToggle">
      <div class="burger" v-bind:class="{ visible: menuIsOpen }">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <!-- <font-awesome-icon icon="bars" class="hamburger" v-on:click="menuIsOpen = true"></font-awesome-icon> -->
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
    //overflow: hidden;
    &:hover {
      opacity: 0.9;
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
    //margin: 50px auto;
    transform: rotate(0deg);
    transition: .5s ease-in-out;
    cursor: pointer;
    margin-top: 8px;
    margin-right: 75px;
  }
  .burger span {
    display: block;
    position: absolute;
    height: 2px;
    width: 100%;
    background: var(--primary-color);
    //border-radius: 9px;
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
    //left: 0px;
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
      //height:50%;
      //transition: 0.5s;
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
          //margin: 20px 0;
          color: var(--background-color-primary);
          opacity: border 0;
          span {
            //margin: 0 50%;
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
              opacity: 0.8;
            }
          }
        }
      }
    }
    .hamburger {
      //position:relative;
      display: inline;
      // margin: 0 -2px 0 0;
      // cursor: pointer;
      // right: 15px;
      // top: 20px;
      // width: 30px;
      // height: 30px;
      // color: var(--header-text-color);
      // z-index: 50;
    }
  }
  .overlay {
    background: rgba(0, 0, 0, 0.01);
    width:100%;
    height:100%;
    top:200px;
    left:0;
    position:fixed;
    z-index:100;
  }
</style>
