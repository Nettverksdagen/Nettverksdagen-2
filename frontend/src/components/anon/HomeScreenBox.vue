<template>
  <div class="home-box">
    <div class="box">
    <img src="@/assets/homebox.svg">
    <div class="wrapper">
      <img class="icon" :src="require(`@/assets/${boxIcon}`)" :alt="boxIconAlt">
      <h3>{{ boxTitle }}</h3>
      <div class="showme">
        <h5>{{ boxText }}</h5>
      </div>
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
  //.home-box {
    //width:340px;
    //height:226px;
    // @media(max-width: 1200px) {
    //   transform: scale(0.8);
    // }
  //}
  .wrapper {
    position:relative;
    // width:inherit;
    // height:inherit;
  }
  .box {
    // width:340px;
    // height:226px;
    width: 100%;
    //height: 100%;
    position: relative;
    //width:inherit;
  }
  .home-box:hover .showme {
    opacity: 1;
  }
  .icon {
    position:relative;
    width:20%;
    height: 20%;
    top: 20%;
    right: 10%;
    filter: invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(94%) contrast(94%);
  }
  h5 {
    font-size: 16px;
    color: var(--primary-color);
    text-decoration: none;
    position: relative;
    top: 52%;
    //bottom: 10%;
    margin-left: 37px;
    margin-right: 40px;
  }
  .home-box:hover h3 {
    opacity: 1;
    transform: translate3d(0, -94px, 0);
    transition: opacity 300ms, transform 400ms;
  }
  h3 {
    position: relative;
    bottom: 13%;
    margin-left: 37px;
    font-size: 28px;
    font-weight: 600;
    color: var(--primary-color);
    text-decoration: none;
    transition: opacity 300ms, transform 400ms;
  }
  .showme {
    opacity: 0;
    transition: opacity 200ms;
  }
</style>
