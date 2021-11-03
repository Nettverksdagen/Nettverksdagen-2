<template>
  <div class="anon-header">
    <div class="content" :class="scrolled ? 'box-shadow' : 'line-border'">
      <b-link :to="'/'" class="logo-link">
        <div class="side">
          <img class="newlogo" v-if="userTheme === 'dark-theme'" src="@/assets/textlogo_dark.png">
          <img class="newlogo" v-else src="@/assets/textlogo_light.png">
        </div>
      </b-link>
      <div class="side">
        <b-nav class="links">
          <b-nav-item class="round-long-button" :to="{name: 'Program'}">PROGRAM</b-nav-item>
          <b-nav-item class="round-long-button" :to="{name: 'Listings'}">STILLINGSANNONSER</b-nav-item>
          <b-nav-item class="round-long-button" :to="{name: 'About'}">OM OSS</b-nav-item>
          <!-- <b-nav-item class="round-long-button" :to="{name: 'About'}">FOR BEDRIFTER</b-nav-item> -->
          <b-nav-item class="round-long-button" :to="{name: 'Contact'}">KONTAKT</b-nav-item>
          <b-nav-item class="round-button" title="Hjem" :to="{name: 'Home'}" active>
            <font-awesome-icon icon="home"></font-awesome-icon>
          </b-nav-item>
          <b-nav-item class="round-button" title="Info" :to="{name: 'About'}">
            <font-awesome-icon icon="info-circle"></font-awesome-icon>
          </b-nav-item>
          <!-- UNCOMMENT TO SHOW "TOGGLE THEME BUTTON"-->
          <!-- <b-nav-item class="round-button" title="Endre tema" v-on:click="toggleTheme">
            <font-awesome-icon icon="adjust"></font-awesome-icon>
          </b-nav-item> -->
       </b-nav>
       <Slider/>
      </div>
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
    const initUserTheme = this.getMediaPreference()
    this.setTheme(initUserTheme)
    console.log(initUserTheme)
  }
}
</script>

<style lang="scss" scoped>
  @import url('https://fonts.googleapis.com/css2?family=Overpass&display=swap');
  .anon-header {
    background:var(--background-color-primary);
    margin:0 auto;
    transition: background 0.5s;
    width: 100%;
    -webkit-position: sticky;
    position: sticky;
    top: 0px;
    z-index: 1;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
  }
  *{
    box-sizing:border-box;
  }
  .newlogo {
    margin: 7px 0 7px 20px;
    height:56px;
    display: inline-block;
    vertical-align: middle;
  }
  .round-button {
    margin: 0 5px 0px 5px;
    width: 40px;
    height: 40px;
    background: var(--background-color-primary);
    color: var(--header-text-color);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 50%;
    border: none;
    text-decoration: none;
    transition: background 0.5s;
    &:hover {
      background:var(--header-text-secondary-color);
    }
  }
  .round-long-button {
    margin: 0 5px 0px 5px;
    height: 100%;
    background: var(--background-color-primary);
    color: var(--header-text-color);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 23px;
    border: none;
    text-decoration: none;
    transition: background 0.5s;
    &:hover {
      background:var(--header-text-secondary-color);
    }
  }
  .logo-link {
    text-decoration:none !important;
  }
  .content {
    width: inherit;
    display:flex;
    flex-direction: row;
    justify-content: space-between;
    align-content:stretch;
    vertical-align: middle;
    flex-wrap: nowrap;
    height:70px;
  }
  .side {
    align-items: center;
    display:flex;
  }
  .links {
    margin: 8px 20px 0 0;
    display:none;
    align-items: center;
    vertical-align: middle;
    @media (min-width: 1000px) {
      display:flex;
      font-size:16px;
      font-family: 'Overpass', sans-serif;
    }
    a {
      color:var(--header-text-color);
    }
  }
  .box-shadow{
    box-shadow: 0px 0px 6px 3px rgba(0,0,0,0.3);
    transition: box-shadow 0.5s;
  }
  .line-border{
    border-bottom: 1px solid var(--line-border-color);
  }
  @media (max-width: 1000px) {
    .logo-link {
      margin-left: -12px;
    }
  }
</style>
