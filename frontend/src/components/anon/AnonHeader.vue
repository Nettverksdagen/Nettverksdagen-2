<template>
  <div class="anon-header">
    <div class="whitebackground">
    </div>
    <div class="content">
      <b-link :to="'/'" class="logo-link">
        <div class="side">
          <!-- <img class="newlogo" v-if="userTheme === 'dark-theme'" src="@/assets/textlogo_dark.png"> -->
          <!-- <img class="newlogo" v-else src="@/assets/textlogo_light.png"> -->
          <img class="newlogo" src="@/assets/nettverksdagenesvg.svg">
        </div>
      </b-link>
      <div class="side">
        <b-nav class="links">
          <b-nav-item :to="{name: 'Program'}"><p>Program 2025</p></b-nav-item>
          <b-nav-item :to="{name: 'Listings'}"><p>{{$t('stillingsannonser')}}</p></b-nav-item>
          <b-nav-item :to="{name: 'About'}"><p>{{$t('omoss')}}</p></b-nav-item>
          <b-nav-item :to="{name: 'Contact'}"><p>{{$t('kontakt')}}</p></b-nav-item>
          <b-nav-item :to="{name: 'Valgomat'}"><p>{{$t('Valgomat')}}</p></b-nav-item>
          <b-nav-item :to="{name: 'FAQ'}"><p>{{$t('FAQ')}}</p></b-nav-item>
          <b-nav-item v-on:click="toggleLanguage"><p>{{$t('lang')}}</p></b-nav-item>
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
import {i18n} from '@/translations/translations.js'
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
    toggleLanguage () {
      if (i18n.locale === 'en') {
        i18n.locale = 'nb'
      } else {
        i18n.locale = 'en'
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
  .anon-header {
    background:var(--background-color-primary);
    margin:0 auto;
    transition: background 0.5s;
    // width: 95%;
    // -webkit-position: fixed;
    position: sticky;
    top: 0px;
    z-index: 10;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    width: 100%;
  }
  *{
    box-sizing:border-box;
  }
  .newlogo {
    margin: 8px 0 8px 5px;
    height:44px;
    display: inline-block;
    vertical-align: middle;
    z-index: 3;
  }
  .newlogo:hover {
    @media(min-width: 768px) {
      opacity: 0.9;
    }
    transition: opacity 300ms, transform 500ms;
  }
  .logo-link {
    text-decoration:none !important;
  }
  .content {
    width: 100%;
    display:flex;
    flex-direction: row;
    height:60px;
  }
  .side {
    align-items: center;
    margin: 0 0 0 auto;
    display:flex;
    float: right;
  }
  .links {
    margin-top: 20px;
    font-weight: 500;
    display: flex;
    flex-direction: row;
    gap: 20px;

    @media (min-width: 992px) {
      display:flex;
      font-size:18px;
      font-weight: 500;
    }
    @media(max-width: 767px) {
      visibility: hidden;
    }
    a {
      //color:var(--primary-color);
      color: black;
      padding: 0;
    }
  }
  p {
    margin: -20px 0 0 0;
    display: inline-block;
    position: relative;
    vertical-align: middle;
  }
  p::after {
    content: "";
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 3px;
    //background-color: var(--primary-color);
    background-color: black;
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
  .whitebackground {
    content: "";
    position: absolute;
    width: 100%;
    height: 60px;
    background-color: var(--background-color-primary);
  }
  .nav-link {
    padding-right: 0;
    padding-left: 2rem;
}
</style>
