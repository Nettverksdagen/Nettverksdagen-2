<template>
  <div class="hero-text">
    <h1 class="mt-3 hero-header">Nettverksdagen 2019</h1>
    <hr class="hr-hero">
    <h2 class="font-weight-light">Glassgården NTNU, 31. januar</h2>
  </div>
</template>

<style lang="scss" scoped>
  .hero-text {
    text-align:center;
    color:#fff;
  }

  .hr-hero {
    border-top: solid 1px white;
    width: 60%;

    @media (min-width: 992px) {
      width: 40%;
    }
  }

  .hero-header {
    text-shadow: 0 3px 5px rgba(0,0,0,0.4);
  }

  /*span {
    font-size: 20px;
  }*/

  h1 {
    font-size: 35px;
  }
  h2 {
    font-size: 25px;
  }
  @media (min-width: 992px) {
    h1 {
      font-size: 50px;
    }
    h2 {
      font-size: 30px;
    }
  }
  @media (min-width: 1200px) {
    h1 {
      font-size: 65px;
    }
    h2 {
      font-size: 35px;
    }
  }
  @media (min-width: 1400px) {
    h1 {
      font-size: 75px;
    }
  }
</style>
