<template>
  <div class="anon-header">
    <div class="content" :class="scrolled ? 'box-shadow' : 'line-border'">
      <b-link :to="'/'" class="logo-link">
        <div class="side">
          <!-- <img class="newlogo" v-if="userTheme === 'dark-theme'" src="@/assets/textlogo_dark.png"> -->
          <!-- <img class="newlogo" v-else src="@/assets/textlogo_light.png"> -->
          <img class="newlogo" src="@/assets/nettverksdagenesvg.svg">
        </div>
      </b-link>
      <div class="side">
        <b-nav class="links">
          <b-nav-item :to="{name: 'Program'}"><p>Program</p></b-nav-item>
          <b-nav-item :to="{name: 'Listings'}"><p>Stillingsannonser</p></b-nav-item>
          <b-nav-item :to="{name: 'About'}"><p>Om oss</p></b-nav-item>
          <!-- <b-nav-item class="round-long-button" :to="{name: 'About'}">FOR BEDRIFTER</b-nav-item> -->
          <b-nav-item :to="{name: 'Contact'}"><p>Kontakt</p></b-nav-item>
          <!-- <b-nav-item class="round-button" title="Hjem" :to="{name: 'Home'}" active>
            <font-awesome-icon icon="home"></font-awesome-icon>
          </b-nav-item>
          <b-nav-item class="round-button" title="Info" :to="{name: 'About'}">
            <font-awesome-icon icon="info-circle"></font-awesome-icon>
          </b-nav-item> -->
          <!-- UNCOMMENT TO SHOW "TOGGLE THEME BUTTON"-->
          <!-- <b-nav-item class="round-button" title="Endre tema" v-on:click="toggleTheme">
            <font-awesome-icon icon="adjust"></font-awesome-icon>
          </b-nav-item> -->
       </b-nav>
       <Slider/>
      </div>
    </div>
    <div class="line">
    </div>
  </div>
</template>

<script>
import Slider from '@/components/common/Slider.vue'
export default {
  data () {
    return {
      scrolled: false,
      userTheme: 'light-theme'
    }
  },
  components: {
    Slider
  },
  methods: {
    handleScroll (event) {
      this.scrolled = window.scrollY > 0
    },
    setTheme (theme) {
      localStorage.setItem('user-theme', theme)
      this.userTheme = theme
      document.documentElement.className = theme
      this.image = this.images[theme]
    },
    toggleTheme () {
      const activeTheme = localStorage.getItem('user-theme')
      console.log(activeTheme)
      if (activeTheme === 'light-theme') {
        this.setTheme('dark-theme')
      } else {
        this.setTheme('light-theme')
      }
    },
    getMediaPreference () {
      const hasDarkPreference = window.matchMedia(
        '(prefers-color-scheme: dark)'
      ).matches
      if (hasDarkPreference) {
        return 'dark-theme'
      } else {
        return 'light-theme'
      }
    }
  },
  created () {
    window.addEventListener('scroll', this.handleScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll)
  },
  mounted () {
    // const initUserTheme = this.getMediaPreference()
    const initUserTheme = 'light-theme'
    this.setTheme(initUserTheme)
    console.log(initUserTheme)
  }
}
</script>

<style lang="scss" scoped>
  @import url('https://fonts.googleapis.com/css2?family=Spline+Sans&display=swap');
  .anon-header {
    background:var(--background-color-primary);
    margin:0 auto;
    transition: background 0.5s;
    width: 100%;
    -webkit-position: sticky;
    position: sticky;
    top: 0px;
    z-index: 10;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    //border-bottom: 2.5px solid var(--line-border-color);
    //padding: 0 30px;
  }
  *{
    box-sizing:border-box;
  }
  .newlogo {
    margin: 8px 0 8px 5px;
    height:44px;
    display: inline-block;
    vertical-align: middle;
  }
  .newlogo:hover {
    opacity: 0.9;
    transition: opacity 300ms, transform 500ms;
  }
  // .round-button {
  //   padding: 2px 0 0 0;
  //   margin: 0 5px 0px 5px;
  //   width: 40px;
  //   height: 40px;
  //   background: var(--background-color-primary);
  //   color: var(--header-text-color);
  //   display: inline-flex;
  //   justify-content: center;
  //   cursor: pointer;
  //   border-radius: 50%;
  //   border: none;
  //   transition: background 0.5s;
  //   &:hover {
  //     background:var(--header-text-secondary-color);
  //   }
  // }
  // .round-long-button {
  //   margin: 0 5px 0px 5px;
  //   padding: 2px 0 0 0;
  //   display: inline-flex;
  //   justify-content: center;
  //   text-align: center;
  //   border-radius: 23px;
  //   border: none;
  //   transition: background 0.5s;
  //   &:hover {
  //     background:var(--header-text-secondary-color);
  //   }
  // }
  .logo-link {
    text-decoration:none !important;
  }
  .content {
    width: 100%;
    display:flex;
    flex-direction: row;
    //justify-content: space-between;
    //align-content:stretch;
    //vertical-align: middle;
    //flex-wrap: nowrap;
    height:60px;
  }
  .side {
    align-items: center;
    margin-left: auto;
    margin-right: -15px;
    display:flex;
    float: right;
  }
  .links {
    margin-top: 20px;
    //align-items: center;
    //vertical-align: middle;
    @media (min-width: 992px) {
      display:flex;
      font-size:18px;
      font-family: 'Spline Sans', sans-serif;
      font-weight: 450;
    }
    @media(max-width: 767px) {
      visibility: hidden;
    }
    a {
      color:var(--primary-color);
    }
  }
  p {
    margin: 5px 0 0 0 0;
    display: inline-block;
    position: relative;
    vertical-align: middle;
  }
  p::after {
    content: "";
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--primary-color);
    opacity: 0;
    transition: transform 100ms;
  }
  p:hover::after {
    opacity: 1;
    transform: translate3d(0, -0.1em, 0);
    transition: opacity 300ms, transform 150ms;
  }
  .line {
    content: "";
    position: absolute;
    width: 100%;
    height: 2.5px;
    background-color: var(--line-border-color);
  }
  // .box-shadow{
  //   box-shadow: 0px 0px 6px 3px rgba(0,0,0,0.3);
  //   transition: box-shadow 0.5s;
  // }
  // @media (max-width: 1000px) {
  //   .logo-link {
  //     margin-left: -12px;
  //   }
  // }
</style>
