<template>
  <div class="loading-page">
    <div class="main-text">
      <h1>Nettverksdagene</h1>
      <h2>2. og 3. mars 2022</h2>
    </div>
    <div class="videoplayer">
      <!-- <img src="@/assets/nvdbackground.svg" alt="Timelapse"/> -->
      <video class ="video" muted loop autoplay>
        <source src="@/assets/timelapse.mp4" type="video/mp4">
      </video>
      <h1>Nettverksdagene</h1>
      <h2>2. og 3. mars 2022</h2>
    </div>
    <!-- <div class="background">
      <img src='@/assets/nvdbackground.svg'/>
    </div>
    <div class="text-box">
      <div  class="home-page-txt">
        <HeroText/>
      </div>
    </div> -->
    <div class="wrapper">
      <div class="hero-content">
        <div class="boxes">
          <b-link :to="'/program'">
            <HomeScreenHex box-title="Stands" box-icon="store-alt-solid.svg" box-text="Glassgården fylles med stands! En god mulighet til å komme i kontakt med mange spennende bedrifter."/>
          </b-link>
          <b-link :to="'/program'">
            <HomeScreenHex box-title="Bankett" box-icon="glass-cheers-solid.svg" box-text="Bli med på bankett og kom i direkte kontakt med representanter fra de ulike bedriftene over en god middag."/>
          </b-link>
          <b-link :to="'/program'">
            <HomeScreenHex box-title="Bedpres" box-icon="utensils-solid.svg" box-text="Det blir holdt flere bedrifts- presentasjoner for de som vil bli bedre kjent med bedriftene."/>
          </b-link>
          <b-link :to="'/program'">
            <HomeScreenHex box-title="Ballongslipp" box-icon="gift-solid.svg" box-text="Vinn flotte premier når Nettverksdagene åpner med ballongslipp."/>
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
import HomeScreenHex from '@/components/anon/HomeScreenHex.vue'
export default {
  components: {
    HeroText,
    HomeScreenBox,
    HomeScreenHex
  }
}
</script>

<style lang="scss" scoped>
  .loading-page {
    width: 100%;
    overflow: hidden;
    margin-top: 20px;
  }
  .main-text {
    margin-top: 100px;
    text-align: center;
    padding-bottom: 100px;
  }
  h1 {
    font-weight: 600;
    font-size: 70px;
    color: white;
    position: absolute;
    top: 500px;
    text-align: center;
    width: 100%;
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
    //margin-top: 20px;
    background-color: white;
    &:hover {
      filter: brightness(70%);
    }
  }
  .background {
    //display: none;
    background: no-repeat;
    width: 200%;
    overflow: hidden;
    //left: 10%;
    top: 10px;
    position: relative;
    z-index: 0;
    @media(min-width: 480px) {
      
    }
    @media(min-width: 768px) {
      width: 100%;
    }
    @media(min-width: 992px) {
      
    }
    @media(min-width: 1200px) {
      
    }
    @media(min-width: 1430px) {
      
    }
  }
  .wrapper {
    //margin-bottom: 200px;
    width:100%;
    position:relative;
    //height:2000px;
    @media(min-width: 480px) {

    }
    @media(min-width: 768px) {

    }
    @media(min-width: 992px) {
      height: 300px;
    }
    @media(min-width: 1200px) {
      height: 400px;
    }
    @media(min-width: 1430px) {

    }
    // @media(min-width: 768px) {
    //   height:450px;
    // }
    // @media(min-width: 992px) {
    //   height:550px;
    // }
    // @media(min-width: 1400px) {
    //   height:650px;
    // }
  }
  .hero-content {
    // display:flex;
    // flex-direction:column;
    top: 160px;
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
    //display:none;
    position: relative;
    width: 100%;
    //overflow-wrap: break-word;
    overflow: hidden;
    margin-top: -180px;
    //left: 10%;
    z-index: 2;
    @media(min-width: 480px) {

    }
    @media(min-width: 768px) {

    }
    @media(min-width: 992px) {

    }
    @media(min-width: 1200px) {

    }
    @media(min-width: 1430px) {
      margin-top: -270px;
    }
    // @media(min-width: 768px) {
    //   margin-bottom:30px;
    // }
    // @media(min-width: 992px) {
    //   margin-bottom:60px;
    // }
  }
  .boxes {
    //display: none;
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
    grid-gap: 10px;

    
    @media(min-width: 480px) {
      // grid-gap: 1.5%;
    }
    @media(min-width: 768px) {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      // grid-gap: 20px;
    }
    @media(min-width: 992px) {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      // grid-gap: 20px;
    }
    @media(min-width: 1200px) {
      grid-template-columns: 1fr 1fr 1fr 1fr;
      // grid-gap: 30px;
    }
    @media(min-width: 1430px) {
      // grid-gap: 50px;
    }
    // @media(max-width: 1200px) {
    //   grid-template-columns: 340px 340px;
    //   grid-template-rows: 226px 226px;
    //   transform:scale(0.8);
    // }
    // grid-gap: 60px;
    // @media(max-width: 767px) {
    //   display:none;
    // }
    a {
       text-decoration: none;
     }
  }
</style>
