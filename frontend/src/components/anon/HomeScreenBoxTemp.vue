<template>
  <div class="home-box">
    <div class="box">
      <img src="@/assets/homeboxtemp.svg">
      <img class="icon" :src="require(`@/assets/${boxIcon}`)" :alt="boxIconAlt">
      <div class="container">
        <h3>{{ boxTitle }}</h3>
      </div>
      <div class="showme">
        <h5>{{ boxText }}</h5>
      </div>
    </div>
  </div>
</template>

<script>
export default{
  props: ['boxIcon', 'boxIconAlt', 'boxTitle', 'boxText']
}
</script>

<style lang="scss" scoped>
  .wrapper {
    position:relative;
    width:100%;
  }
  .box {
    width: 100%;
    position: relative;
  }
  .home-box:hover .showme {
    @media(min-width: 1430px) {
      opacity: 1;
      transition: opacity 400ms;
      transition-delay: 150ms;
    }
  }
  .container {
    width: 100%;
    height: 100%;
  }
  .icon {
    position: absolute;
    top: 30px;
    right: 30px;
    width: 10%;
    z-index: 5;
    filter: brightness(150%);
    transition-duration: 400ms;
    @media(max-width: 768px) {
      top: 10px;
      right: 20px;
    }
    @media(max-width: 992px) {
      top: 15px;
      right: 20px;
    }
  }

  .home-box:hover .icon{
    filter: brightness(200%);
    transition-duration: 400ms;
  }

  h5 {
    font-size: 18px;
    color: var(--primary-color);
    text-decoration: none;
    position: absolute;
    top: 59%;
    margin-left: 47px;
    margin-right: 30px;
    
  }
  .home-box:hover h3 {
    transition: opacity 300ms, transform 400ms;
    @media(min-width: 1430px) {
      transform: translate3d(0, -150%, 0);
    }
  }
  h3 {
    position: absolute;
    margin-top: -11%;
    margin-left: 4%;
    font-size: 26px;
    font-weight: 600;
    color: var(--primary-color);
    text-decoration: none;
    transition: opacity 300ms, transform 400ms;
    overflow-wrap: break-word;
    @media(min-width: 576px) {
      margin-top: -12%;
      margin-left: 0%;
      font-size: 35px;
    }
    @media(min-width: 768px) {
      margin-top: -11%;
      margin-left: 2%;
      font-size: 35px;
    }
    @media(min-width: 992px) {
      margin-top: -9%;
      margin-left: 2%;
      font-size: 40px;
    }
    @media(min-width: 1200px) {
      margin-top: -7%;
      margin-left: 2%;
      font-size: 40px;
    }
    @media(min-width: 1430px) {
      font-size: 54px;
      margin-top: -7%;
      margin-left: -7%;
      font-size: 50px;
    }
  }
  .showme {
    transition: opacity 100ms;
    transition-delay: 0ms;
    opacity: 0;
  }

</style>
