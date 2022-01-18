<template>
  <div class="home-box">
    <div class="box">
    <img src="@/assets/homebox.svg">
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
    height: 100%;
  }
  .box {
    width: 100%;
    position: relative;
  }
  .home-box:hover .showme {
    @media(min-width: 1430px) {
      opacity: 1;
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
    width: 20%;
    z-index: 5;
    filter: invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(94%) contrast(94%);
  }
  h5 {
    font-size: 18px;
    color: var(--primary-color);
    text-decoration: none;
    position: absolute;
    top: 47%;
    margin-left: 37px;
    margin-right: 30px;
  }
  .home-box:hover h3 {
    transition: opacity 300ms, transform 400ms;
    @media(min-width: 1430px) {
      transform: translate3d(0, -270%, 0);
    }
  }
  h3 {
    position: absolute;
    margin-top: -20%;
    margin-left: 7%;
    font-size: 26px;
    font-weight: 600;
    color: var(--primary-color);
    text-decoration: none;
    transition: opacity 300ms, transform 400ms;
    overflow-wrap: break-word;
    @media(min-width: 1430px) {
      font-size: 30px;
    }
  }
  .showme {
    transition: opacity 200ms;
    opacity: 0;
  }
</style>
