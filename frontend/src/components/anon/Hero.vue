<template>
  <div class="hero" :style="{'background-image': 'url(' + require('@/assets/hero_blur.jpg') + ')'}">
  <!-- <div class="hero" :style="{'background-video': 'url(' + require('@/assets/timelapse.mp4') + ')'}"> -->
    <video loop muted autoplay class="timelapse">
      <source src="@/assets/timelapse.mp4" type="video/mp4">
    </video>
    <div class="sponsor-banner kjeldsberg-banner">
      <a href="http://kjeldsbergkaffe.no/" target="_blank" rel="noopener noreferrer">
        <b-row>
          <b-col cols="12" md="6" class="sponsor-banner-text align-middle">
            <h3 class="font-weight-bold">Takk til Kjeldsberg Kaffe!</h3>
            <span>Vi takker Kjeldsberg Kaffe for forsyning av kaffe under hele Nettverksdagene 2021!</span>
          </b-col>
          <b-col cols="12" md="6" class="text-center">
            <img class="logo-kjeldsberg float-md-right" src="@/assets/textlogo_dark.png">
          </b-col>
        </b-row>
      </a>
    </div>
    <div class="wrapper">
      <div class="hero-content">
        <HeroText class="hero-txt"/>
        <div class="hexes">
          <b-link :to="'/program'">
            <HeroHexBox hex-title="Ballongslipp" hex-icon="balloon.svg">
              <!-- Det blir ballongslipp der du kan vinne flotte premier!
              I tillegg har vi mange andre konkurranser i løpet av dagen. -->
            </HeroHexBox>
          </b-link>
          <b-link :to="'/program'">
            <HeroHexBox hex-title="Stands" hex-icon="transfer.svg">
              <!--Hele Glassgården fylles med stands! Her har du mulighet for å komme i kontakt med mange spennende bedrifter.
              Standkartet finner du på programsiden. -->
            </HeroHexBox>
          </b-link>
          <b-link :to="'/program'">
            <HeroHexBox hex-title="Bedriftpresentasjoner" hex-icon="presentation.svg">
              <!--Det blir holdt flere bedriftpresentasjoner for de som vil bli bedre kjent med bedriftene.
              Påmelding gjøres på Facebook-siden vår.-->
            </HeroHexBox>
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
import HeroHexBox from '@/components/anon/HeroHexBox.vue'
export default {
  components: {
    HeroText,
    HeroHexBox
  }
}
</script>

<style lang="scss" scoped>
  .hero {
    background: no-repeat top;
    background-size: auto 100%;
    margin: 20px;
  }
  .timelapse {
    margin: 2rem;
    border-radius: 0.5rem;
    width: 1000px;
    height: 100%;
    // position: absolute;
    padding: 0;
    margin: 0;
    left: 0px;
    top: 0px;
    overflow: hidden;
    &:hover {
      background-color: #fff;
      box-shadow: 0 5px 10px rgba(0,0,0,0.20), 0 5px 10px rgba(0,0,0,0.18);
    }
  }
  .wrapper {
    width:100%;
    position:relative;
    overflow:hidden;
    height:300px;
    @media(min-width: 768px) {
      height:450px;
    }
    @media(min-width: 992px) {
      height:550px;
    }
    @media(min-width: 1400px) {
      height:650px;
    }
  }
  .hero-content {
    display:flex;
    flex-direction:column;
    position:absolute;
    top:0;
    justify-content: center;
    height:100%;
    width:100%;
    padding: 0 11px;
    @media (min-width: 1200px) {
      padding: 0 100px;
    }
    @media (min-width: 1400px) {
      padding: 0 200px;
    }
  }
  .hero-text {
    @media(min-width: 768px) {
      margin-bottom:30px;
    }
    @media(min-width: 992px) {
      margin-bottom:60px;
    }
  }
  .hexes {
    display:flex;
    flex-direction:row;
    justify-content: space-between;
    @media(max-width: 767px) {
      display:none;
    }

    a {
      text-decoration: none;
    }
  }
  h2 {
    font-size: 2.5rem;
  }
  .sponsor-banner {
    width: 400px;
    margin: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.16), 0 2px 5px rgba(0,0,0,0.15);
    transition: 0.2s;

    &:hover {
      box-shadow: 0 5px 10px rgba(0,0,0,0.20), 0 5px 10px rgba(0,0,0,0.18);
    }

    a {
      text-decoration:none;
      color: inherit;
    }

    @media(max-width: 576px) {
      margin: 1rem;
    }
  }
  .sponsor-banner-text {
    padding: 3rem 4rem;

    h3 {
      color: #221e1f;
      margin-bottom: 0.5rem;
      font-size: 1.9rem;
    }

    span {
      font-size: 1.2rem;
    }

    @media(max-width: 576px) {
      padding: 1.5rem 2.5rem;

      span {
        font-size: 0.9rem;
      }

      h3 {
        font-size: 1.5rem;
      }
    }

    @media(max-width: 768px) {
      padding-bottom: 0;
    }

  }
  .no-padding-top {
    padding-top:0;
  }
  .kjeldsberg-banner {
    background-color: #1f4945;
  }
  .logo-kjeldsberg {
    height: 3rem;
    padding: 0.5rem 3rem 1rem 3rem;

    @media(max-width: 576px) {
      height: 7.5rem;
      padding: 0 1rem 1rem 1rem;
    }
  }
</style>
