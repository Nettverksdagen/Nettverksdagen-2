<template>
  <div class="hero-hex">
    <div class="wrapper">
      <img class="hex" src="@/assets/hexagon.png">
      <img class="icon" :src="require(`@/assets/${hexIcon}`)" :alt="hexIconAlt">
    </div>
  </div>
</template>

<script>
export default{
  props: ['hexIcon', 'hexIconAlt']
}
</script>

<style lang="scss" scoped>
  .hero-hex {
    width:100px;
    height:100px;
    @media(min-width: 1200px) {
      width:150px;
      height:150px;
    }
  }
  .wrapper {
    position:relative;
    width:100%;
    height:100%;
  }
  .hex {
    top:0;
    left:0;
    position:absolute;
    width:100%;
  }
  .icon {
    position:absolute;
    width:40%;
    top:30%;
    left:30%;
  }
</style>
