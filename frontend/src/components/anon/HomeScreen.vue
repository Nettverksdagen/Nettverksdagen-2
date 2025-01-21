<template>
  <div class="loading-page">
    <b-row class="firstrow">
        <div class="col-12 splash-text" :style="{'background-image': 'url(' + require('@/assets/iphonebakgrunn.svg') + ')'}">
            <div class="hometext">
                <h3>{{$t('homescreen.fremtidig')}}</h3>
                <h1>{{$t('nettverksdagene')}}</h1>
                <h2>21.01-23.01 2025</h2>
            </div>
        </div>
        <div class="col-12 homevideo">
            <div class="video-container">
              <video class="video" muted playsinline loop autoplay>
                  <source src="@/assets/timelapse.mp4" type="video/mp4">
              </video>
            </div>
            <img class="overlay" src="@/assets/background_overlay.png">
        </div>
    </b-row>
    <div class="boxes">
      <b-link :to="{name: 'Home', hash: '#stand-map'}" @click.native="scrollToId('stand-map')">
        <HomeScreenBox box-title="Stands" box-icon="store-alt-solid.svg" :box-text="$t('glassgårdentext')"/>
      </b-link>
      <b-link :to="'/program'">
        <HomeScreenBox :box-title="$t('avslutningsmiddagtitle')" box-icon="glass-cheers-solid.svg" :box-text="$t('programtext')"/>
      </b-link>
      <b-link :to="'/program'">
        <HomeScreenBox :box-title="$t('bedpresword')" box-icon="utensils-solid.svg" :box-text="$t('bedpres2')"/>
      </b-link>
      <b-link :to="'/stillinger' /* Denne filstien er definert i router/index.js */ ">
        <HomeScreenBox :box-title="$t('stillingsannonser_card_title')" box-icon="interview-icon.svg" :box-text="$t('stillingsannonser_card_text')"/>
      </b-link>
      <!-- <b-link :to="'/program'">
        <HomeScreenBox :box-title="$t('interviews')" box-icon="interview-icon.svg" :box-text="$t('interviews2')"/>
      </b-link> -->
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
      var element = document.getElementById(id);
      var headerOffset = 80; // Pure guess. TODO: should be replaced with a more accurate value for the header height
      var elementPosition = element.getBoundingClientRect().top;
      var offsetPosition = elementPosition + window.scrollY - headerOffset;
    
      window.scrollTo({
          top: offsetPosition,
          behavior: "smooth"
      });
    }
  }
}
</script>

<style lang="scss" scoped>
  $tiny-width: 300px;
  $small-width: 500px;
  $medium-width: 768px;
  $large-width: 992px;
  $largest-width: 1400px;

  .loading-page {
    width: 100%;
    // overflow: hidden;
    margin-top: 0px;
  }
  .splash-text {
    background: no-repeat top;
    padding: 0;
    // background-size: 95% auto;

    // TODO: Replace all hard-coded values with variables, also make them dependent on rem units rather than pixels
    --padding-bottom: 100px;
    --background-size: 361px;
    @media (min-width: $medium-width) {
      --background-size: 642px;
      --padding-bottom: 140px;
    }
    @media (min-width: $large-width) {
      --background-size: 905px;
      --padding-bottom: 220px;
    }
    @media(min-width: $largest-width) {
      --background-size: 700px;
      --padding-bottom: 200px;
      top: 10px;
    }
    background-size: var(--background-size) auto;
    padding-bottom: var(--padding-bottom);

    // This was part of the column styling before (col-xl-6 from bootstrap framework), but was removed because it was using incorrect breakpoints
    @media (min-width: $largest-width) {
      flex: 0 0 50%;
    }
  }
  .firstrow {
    margin: 0; // Removes the default margin from the b-row element
  }
  .hometext {
    // z-index: 10; // To make sure the text is on top of the background
    --home-text-margin-top: 85px;
    @media(min-width: $medium-width) {
      --home-text-margin-top: 140px;
    }
    @media(min-width: $large-width) {
      --home-text-margin-top: 220px;
    }
    @media(min-width: $largest-width) {
      --home-text-margin-top: 140px;
    }
    margin-top: var(--home-text-margin-top);
  }
  .homevideo {
    display: none;
    // padding: 0 !important;
    position: relative;
    // overflow: hidden;
    // TODO: Replace video overlay with a clipping mask

    padding: 0 0.5rem; // Very hacky way to make the video not show any artefacts outside the container

    // This was part of the column styling before (col-xl-6 from bootstrap framework), but was removed because it was using incorrect breakpoints
    @media (min-width: $largest-width) {
      flex: 0 0 50%;
    }

    // Only show the video on larger screens
    @media(min-width: $largest-width) {
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
  }
  .video-container {
    overflow: hidden; // Very hacky way to make the video not show any artefacts outside the container
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .video {
    width: 100%;
    transform: scale(1.4); // Arbitrary scaling to make the video fill the overlay
    transform-origin: 0 50%; // So that the scaling happens from the left edge
    
    border-radius: 30px;
  }
  .overlay {
    position: absolute;
    width: 100%;
    height: 100%;
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
    @media(min-width: $medium-width) {
      font-size: 88px;
    }
    @media(min-width: $largest-width) {
      text-align: left;
      font-size: 88px;
      margin-left: -4px;
    }
  }
  h3 {
    display: none;
    color: var(--primary-color);
    text-align: center;
    @media(min-width: $medium-width) {
        display: block;
        text-align: center;
        font-size: 36px;
    }
    @media(min-width: $largest-width) {
        text-align: left;
        font-size: 28px;
    }
  }
  h2 {
    text-align: center;
    color: var(--primary-color);
    font-size: 28px;
    font-weight: 600;
    @media(min-width: $medium-width) {
        text-align: center;
        font-size: 32px;
    }
    @media(min-width: $largest-width) {
        text-align: right;
        margin-top: -5px;
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
  }
  .boxes {
    // align-self: center;
    margin: 0 auto; // Hack to center the boxes
    width: fit-content; // To prevent the box-container from stretching to the full width

    display: grid;
    grid-template-columns: repeat(2, 1fr);
    width: clamp(300px, 90%, 100%); // Numbers chosen a little at random

    --gap-size: 5px;
    --font-size: 0.6rem;
    --icon-size: 30px;
    @media(min-width: $small-width) {
      --gap-size: 10px;
      --font-size: 0.8rem;
      --icon-size: 35px;
    }
    @media(min-width: $medium-width) {
      --gap-size: 20px;
      --font-size: 1.1rem;
      --icon-size: 40px;
    }
    @media(min-width: $large-width) {
      --gap-size: 30px;
      --font-size: 1.2rem;
      --icon-size: 45px;
    }
    gap: var(--gap-size);
    font-size: var(--font-size);

    // Could be useful for larger screens
    @media(min-width: $largest-width) {
      --font-size: 1.2rem;
      --icon-size: 50px;
      grid-template-columns: repeat(4, 1fr);
    }

    // Prevent text in boxes from showing underline
    a {
      text-decoration: none;
    }
  }
  .temp-link {
    grid-column: span 2;
    @media(min-width: $largest-width) {
      grid-column: span 4;
    }
  }
</style>
