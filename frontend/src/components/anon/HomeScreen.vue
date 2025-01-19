<template>
  <div class="loading-page">
    <b-row class="firstrow">
        <div class="col-12 col-xl-6 firsthalf" :style="{'background-image': 'url(' + require('@/assets/iphonebakgrunn.svg') + ')'}">
            <div class="hometext">
                <h3>{{$t('homescreen.fremtidig')}}</h3>
                <h1>{{$t('nettverksdagene')}}</h1>
                <h2>21.01-23.01 2025</h2>
            </div>
        </div>
        <div class="col-12 col-lg-6 homevideo">
            <video class ="video" muted loop autoplay>
                <source src="@/assets/timelapse.mp4" type="video/mp4">
            </video>
            <img class="overlay" src="@/assets/background_overlay.png">
        </div>
    </b-row>
    <div class="boxes">
      <router-link :to="{name: 'Home', hash: '#stand-map'}" @click.native="scrollToId('stand-map')">
        <HomeScreenBox box-title="Stands" box-icon="store-alt-solid.svg" :box-text="$t('glassgårdentext')"/>
      </router-link>
      <b-link :to="'/program'">
        <HomeScreenBox :box-title="$t('avslutningsmiddagtitle')" box-icon="glass-cheers-solid.svg" :box-text="$t('programtext')"/>
      </b-link>
      <b-link :to="'/program'">
        <HomeScreenBox :box-title="$t('bedpresword')" box-icon="utensils-solid.svg" :box-text="$t('bedpres2')"/>
      </b-link>
      <b-link :to="'/program'">
        <HomeScreenBox :box-title="$t('interviews')" box-icon="interview-icon.svg" :box-text="$t('interviews2')"/>
      </b-link>
    </div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import HomeScreenBox from '@/components/anon/HomeScreenBox.vue'
export default {
  components: {
    HomeScreenBox,
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
    height: 350px;
    @media(min-width: 500px) {
        height: 400px;
    }
    @media(min-width: 600px) {
        height: 500px;
    }
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
    // align-self: center;
    margin: 0 auto; // Hack to center the boxes
    width: fit-content; // To prevent the box-container from stretching to the full width

    display: grid;
    grid-template-columns: repeat(2, 1fr);
    width: clamp(300px, 90%, 1024px); // Numbers chosen a little at random

    $tiny-width: 300px;
    $small-width: 500px;
    $medium-width: 768px;
    $large-width: 992px;
    $largest-width: 1200px;

    --gap-size: 5px;
    --font-size: 0.6rem;
    --icon-size: 30px;
    @media(min-width: $small-width) {
      --gap-size: 10px;
      --font-size: 0.8rem;
      --icon-size: 40px;
    }
    @media(min-width: $medium-width) {
      --gap-size: 20px;
      --font-size: 1.4rem;
      --icon-size: 50px;
    }
    @media(min-width: $large-width) {
      --gap-size: 30px;
      --font-size: 1.6rem;
      --icon-size: 60px;
    }
    gap: var(--gap-size);
    font-size: var(--font-size);

    // Could be useful for larger screens
    // @media(min-width: --largest-width) {
    //   grid-template-columns: repeat(4, 1fr);
    // }
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
