<template>
  <div class="home-box">
    <div class="hex">
        <img class="hexagon" src="@/assets/hexagon.png">
        <img class="icon" :src="require(`@/assets/${boxIcon}`)" :alt="boxIconAlt">
    </div>
    <HeroHex/>
      <div class="title">
        <h3>{{ boxTitle }}</h3>
      </div>
      <div class="text">
        <h5>{{ boxText }}</h5>
      </div>
  </div>
</template>

<script>
export default{
  props: ['boxIcon', 'boxIconAlt', 'boxTitle', 'boxText']
}
</script>

<style lang="scss" scoped>
  .home-box {
    width:100%;
    @media(max-width: 1200px) {
      transform: scale(0.8);
    }
    text-align: center;
  }
  .hex {
    position: relative;
    width: 70px;
  }
  .hexagon {
      filter: brightness(0) invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(94%) contrast(94%);
      position: absolute;
      width: 70px;
      left: 0;
      top: 0;
      width: 100%;
  }
  .icon {
    position: absolute;
    width:40%;
    top:30%;
    left:30%;
    filter: brightness(0) invert(1);
  }
  h3 {
    margin-top: 10px;
    position: relative;
    text-decoration: none;
    font-size: 24px;
    font-weight: 600;
    color: var(--primary-color);
  }
  h5 {
    margin-top: 10px;
    position: relative;
    text-decoration: none;
    font-size: 18px;
    font-weight: normal;
    color: var(--primary-color);
  }
</style>
