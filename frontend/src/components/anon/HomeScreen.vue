<template>
  <div class="loading-page">
    <div class="background">
      <!-- <img src='@/assets/nvdbackground.svg'/> -->
    </div>
    <HeroText class="home-page-txt"/>
    <div class="wrapper">
      <div class="hero-content">
        <div class="boxes">
          <b-link :to="'/program'">
            <HomeScreenBox box-title="Stands" box-icon="store-alt-solid.svg" box-text="Glassgården fylles med stands! En god mulighet til å komme i kontakt med mange spennende bedrifter."/>
          </b-link>
          <b-link :to="'/program'">
            <HomeScreenBox box-title="Bankett" box-icon="glass-cheers-solid.svg" box-text="Bli med på bankett og kom i direkte kontakt med representanter fra de ulike bedriftene over en god middag."/>
          </b-link>
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
export default {
  components: {
    HeroText,
    HomeScreenBox
  }
}
</script>

<style lang="scss" scoped>
  .loading-page {
    width: 100%;
  }
  .background {
    background: no-repeat;
    width: 80%;
    left: 10%;
    top: 100px;
    position: absolute;
    z-index: 0;
  }
  .wrapper {
    margin-bottom: 200px;
    width:100%;
    position:relative;
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
    // display:flex;
    // flex-direction:column;
    top: 530px;
    position:absolute;
    //top:200px;
    //left: 10%;
    // right: 0;
    // justify-content: center;
    // height:100%;
    width:100%;
    left:0%;
    // padding: 0 11px;
    // @media (min-width: 1200px) {
    //   padding: 0 100px;
    // }
    // @media (min-width: 1400px) {
    //   padding: 0 200px;
    // }
  }
  .home-page-txt {
    display:none;
    position: absolute;
    width: 300px;
    overflow-wrap: break-word;
    //overflow: hidden;
    top: 220px;
    //left: 10%;
    z-index: 2;
    // @media(min-width: 768px) {
    //   margin-bottom:30px;
    // }
    // @media(min-width: 992px) {
    //   margin-bottom:60px;
    // }
  }
  .boxes {
    // justify-content: center;
    // align-items: center;
    width: 100%;
    //width: inherit;
    //padding: 10px;
    //flex-direction:row;
    //justify-content: space-between;
    //margin-left: 10%;
    display:inline-grid;
    //grid-auto-flow: column;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    //grid-gap: 100px;
    @media(max-width: 1200px) {
      grid-template-columns: 340px 340px;
      grid-template-rows: 226px 226px;
      transform:scale(0.8);
    }
    grid-gap: 60px;
    @media(max-width: 767px) {
      display:none;
    }
    a {
       text-decoration: none;
     }
  }
</style>
