<template>
  <div class="hero">
    <div class="wrapper">
      <img class="hero-img" src="@/assets/hero_blur.jpg">
      <div class="hero-content">
        <HeroText class="hero-txt"/>
        <div class="hexes">
          <HeroHexBox hex-title="Ballongslipp" hex-icon="balloon.svg">
            Det blir ballongslipp der du kan vinne flotte premier!
            I tillegg har vi mange andre konkurranser i løpet av dagen.
          </HeroHexBox>
          <HeroHexBox hex-title="Stands" hex-icon="transfer.svg">
            Hele glassgården fylles med stands! Her har du mulighet for å komme i kontakt med mange spennende bedrifter.
          </HeroHexBox>
          <HeroHexBox hex-title="Bedriftpresentasjoner" hex-icon="presentation.svg">
            Det blir holdt flere bedriftpresentasjoner for de som vil bli bedre kjent med bedriftene.
            Påmelding gjøres på facebook-siden vår.
          </HeroHexBox>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import HeroText from '@/components/HeroText.vue'
import HeroHexBox from '@/components/HeroHexBox.vue'
export default {
  components: {
    HeroText,
    HeroHexBox
  }
}
</script>

<style lang="scss" scoped>
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
    @media(max-width: 768px) {
      display:none;
    }
  }
</style>
