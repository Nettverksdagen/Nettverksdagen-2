<template>
  <div class="home-box">
    <div class="box">
      <img src="@/assets/homebox.svg">
      <img class="icon" :src="require(`@/assets/${boxIcon}`)" :alt="boxIconAlt">
      <div class="container">
        <div class="fancy-text">
          <h3>{{ boxTitle }}</h3>
          <h5 class="showme">{{ boxText }}</h5>
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
  .wrapper {
    position:relative;
    width:100%;
  }
  .box {
    width: 100%;
    height: 100%;
    display: flex;
    position: relative;
  }
  // .home-box:hover .showme {
  //   @media(min-width: 1430px) {
  //     opacity: 1;
  //     transition: opacity 400ms;
  //     transition-delay: 150ms;
  //   }
  // }
  .container {
    position: absolute;
    top: 0;
    // padding: 1em;
    width: 100%;
    height: 100%;
    display: flex;
  }
  .fancy-text {
    margin: 1em;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: fit-content;
    align-self: flex-end;
    // height: 100%;
    justify-content: flex-end;
    transform: translateY(100%);
  }
  .icon {
    position: absolute;
    top: 30px;
    right: 30px;
    width: 20%;
    z-index: 5;
    filter: invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(94%) contrast(94%);
    transition-duration: 400ms;
  }

  .home-box:hover .icon{
    filter: invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(130%) contrast(94%);
  }

  .home-box:hover {
    h3, .showme, .fancy-text {
      transition: opacity 300ms 200ms, transform 400ms;
      transform: translateY(0);
    }
    .showme {
      opacity: 1;
    }
  }
  h3 {
    transform: translateY(-100%);
    font-size: 26px;
    font-weight: 600;
    color: var(--primary-color);
    text-decoration: none;
    overflow-wrap: break-word;
    align-self: flex-end;

    @media(min-width: 1430px) {
      font-size: 30px;
    }
  }
  h3, .showme, .fancy-text {
    transition: opacity 300ms, transform 400ms 150ms;
  }
  h3, .showme {
    align-self: start;
  }
  .showme {
    // transition: opacity 100ms;
    // transition-delay: 0ms;
    opacity: 0;

    font-size: 18px;
    color: var(--primary-color);
    text-decoration: none;
  }

</style>
