<template>
  <div class="loading-page">
    <b-row class="firstrow">
        <div class="col-12 col-xl-6 firsthalf" :style="{'background-image': 'url(' + require('@/assets/iphonebakgrunn.svg') + ')'}">
            <div class="hometext">
                <h3>Møt din fremtidige arbeidsgiver på</h3>
                <h1>Nettverksdagene</h1>
                <h2>31.01-02.02 2023</h2>
            </div>
        </div>  
        <div class="col-12 col-lg-6 homevideo">
            <video class ="video" muted loop autoplay>
                <source src="@/assets/timelapse.mp4" type="video/mp4">
            </video>
            <img class="overlay" src="@/assets/background_overlay.png">
        </div>
    </b-row>
    <div class="wrapper">
      <div class="hero-content">
        <div class="boxes">
          <b-link :to="'/2022'" class="temp-link">
            <HomeScreenBoxTemp box-title="Fjorårets program" box-icon="nettverksdagenesvg.svg" box-text="Nettverksdagene 2023 Trykk her for å se hvilke arrangementer som foregikk under Nettverksdagene 2022!"/>
          </b-link>
          <b-link :to="'/program'">
            <HomeScreenBox box-title="Stands" box-icon="store-alt-solid.svg" box-text="Glassgården fylles med stands! Kom i kontakt med mange spennende bedrifter."/>
          </b-link>
          <router-link :to="{name: 'Program', hash: '#bankett'}" @click.native="scrollToId('bankett')">
            <HomeScreenBox box-title="Bankett" box-icon="glass-cheers-solid.svg" box-text="Nettverksdagene avsluttes med en bankett på Thon Hotel Prinsen."/>
          </router-link>
          <b-link :to="'/program'">
            <HomeScreenBox box-title="Bedpres" box-icon="utensils-solid.svg" box-text="Det blir holdt flere bedrifts- presentasjoner for de som vil bli bedre kjent med bedriftene."/>
          </b-link>
          <b-link :to="'/program'">
            <HomeScreenBox box-title="Ballongslipp" box-icon="gift-solid.svg" box-text="Vinn flotte premier når Nettverksdagene åpner med ballongslipp."/>
          </b-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import HeroText from '@/components/anon/HeroText.vue'
import HomeScreenBox from '@/components/anon/HomeScreenBox.vue'
import HomeScreenBoxTemp from './HomeScreenBoxTemp.vue'
export default {
  components: {
    HeroText,
    HomeScreenBox,
    HomeScreenBoxTemp
  },
  methods: {
    scrollToId (id) {
      document.getElementById(id).scrollIntoView()
    }
  }
}
</script>

<style lang="scss" scoped>
  .loading-page {
    width: 100%;
    overflow: hidden;
    margin-top: 0px;
  }
  .firstrow {
    height: 280px;
    @media(min-width: 768px) {
        height: 630px;
    }
    @media(min-width: 992px) {
        height: 670px;
    }
    @media(min-width: 1200px) {
        height: 440px;
    }
    @media(min-width: 1430px) {
        height: 520px;
    }
  }
  .firsthalf {
    background: no-repeat top;
    background-size: 95% auto;
    @media(min-width: 1430px) {
      background-size: 95% auto;
      top: 10px;
    }
  }
  .hometext {
    margin-top: 85px;
    z-index: 10;
    @media(min-width: 768px) {
        margin-top: 140px;
    }
    @media(min-width: 992px) {
        margin-top: 220px;
    }
    @media(min-width: 1200px) {
        margin-top: 110px;
    }
    @media(min-width: 1430px) {
        margin-top: 140px;
    }
  }
  .homevideo {
      display: none;
      margin-top: 90px;
      @media(min-width: 1430px) {
          display: block;
      }
  }
  .video {
    transform: scale(1.1);
    margin-left: 30px;
    overflow: hidden;
  }
  .overlay {
    position: absolute;
    top: -125px;
    left: 10px;
    width: 98%;
    height: 120%;
    align-content: center;
  }
  .main-text {
    margin-top: 100px;
    text-align: center;
    padding-bottom: 100px;
  }
  h1 {
    text-align: center;
    font-weight: 700;
    font-size: 42px;
    color: var(--primary-color);
    z-index: 10;
    @media(min-width: 768px) {
        font-size: 90px;
    }
    @media(min-width: 1200px) {
        text-align: left;
        font-size: 70px;
        margin-left: -4px;
        margin-top: -15px;
    }
    @media(min-width: 1430px) {
        text-align: left;
        font-size: 90px;
        margin-left: -4px;
    }
  }
  h3 {
    display: none;
    color: var(--primary-color);
    text-align: center;
    @media(min-width: 768px) {
        display: block;
        text-align: center;
        font-size: 36px;
    }
    @media(min-width: 1200px) {
        text-align: left;
        font-size: 28px;
    }
  }
  h2 {
    text-align: center;
    color: var(--primary-color);
    font-size: 28px;
    font-weight: 600;
    @media(min-width: 768px) {
        text-align: center;
        font-size: 32px;
    }
    @media(min-width: 1200px) {
        text-align: right;
        margin-top: -5px;
    }
  }
  .videoplayer {
    height: 464px;
  }
  .video {
    width: 100%;
    height: inherit;
    position: relative;
    border-radius: 30px;
    overflow: hidden;
    background-color: white;
    &:hover {
      filter: brightness(70%);
    }
  }
  .background {
    position: absolute;
    top: 0;
    width: 100%;
    margin: auto 0;
    z-index: 1;
  }
  .image {
    width: 100%;
    z-index: 1;
  }
  .iphonebubbles {
    width: 100%;
    top: 40px;
    position: absolute;
    left: 0;
    z-index: 1;
  }
  .zindex1 {
    z-index: 1;
  }
  .zindex2 {
    z-index: 2;
  }
  .excitedpeople {
    position: absolute;
    width: 100%;
    border-radius: 20px;
    z-index: 2;
  }
  .sizeiphoneimage {
    width: 90%;
    max-width: 100%;
    border-radius: 20px;
    position: absolute;
    top: -67px;
  }
  .wrapper {
    width:100%;
    position:relative;
    height: 120px;
    @media(min-width: 768px) {
      height: 620px;
    }
    @media(min-width: 1200px) {
      height: 400px;
    }
    @media(min-width: 1430px) {
      height: 500px;
    }
  }
  .hero-content {
    position:absolute;
    height:300px;
    width:100%;
    left:0%;
  }
  .home-page-txt {
    position: relative;
    width: 100%;
    overflow: hidden;
    margin-top: -180px;
    z-index: 2;
    @media(min-width: 1430px) {
      margin-top: -270px;
    }
  }
  .boxes {
    width: 100%;
    margin-left: 0%;
    display: inline-grid;
    grid-template-rows: 1fr 1fr 1fr;
    grid-template-columns: 1fr 1fr;
    height: inherit;
    grid-gap: 30px;
    @media(min-width: 768px) {
      width: 60%;
      margin-left: 20%;
    }
    @media(min-width: 992px) {
      width: 70%;
      margin-left: 15%;
    }
    @media(min-width: 1200px) {
      grid-template-rows: 1fr 1fr;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      display:inline-grid;
      width: 100%;
      margin-left: 0%;
    }
    a {
       text-decoration: none;
     }
    }
  .temp-link {
    grid-column: span 2;
    @media(min-width: 1200px) {
      grid-column: span 4;
    }
  }
</style>
