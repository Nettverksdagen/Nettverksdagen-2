<template>
  <div class="hero-text">
    <div class="top">
      <h3>Møt din fremtidige arbeidsgiver på</h3>
    </div>
    <div class="mid">
      <h1>Nettverksdagene</h1>
    </div>
    <div class="bottom">
      <h2>2. og 3. mars 2022</h2>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .hero-text {
    color: var(--primary-color);
    width: 100%;
    text-align: center;
    @media(min-width: 768px) {
      width: 60%;
    }
    @media(min-width: 992px) {
      width: 70%;
    }
    @media(min-width: 1200px) {
      width: 50%;
    }
  }
  .hero-header {
    text-shadow: 0 3px 5px rgba(0,0,0,0.4);
  }
  h1 {
    font-size: 10vw;
    font-weight: 700;
    //margin-left: -4px;
    @media(min-width: 480px) {
      font-size: 10vw;
    }
    @media(min-width: 768px) {
      font-size: 40px;
    }
    @media(min-width: 992px) {
      font-size: 60px;
    }
    @media(min-width: 1200px) {
      font-size: 80px;
    }
    @media(min-width: 1430px) {
      font-size: 90px;
    }
  }
  h2 {
    font-size: 7vw;
    font-weight: 400;
    margin-top: 12px;
    @media(min-width: 480px) {
      font-size: 6.5vw;
    }
    @media(min-width: 768px) {
      font-size: 30px;
      text-align: right;
    }
    @media(min-width: 992px) {
      font-size: 34px;
    }
    @media(min-width: 1200px) {
      font-size: 40px;
    }
    @media(min-width: 1430px) {
      font-size: 44px;
    }
  }
  h3 {
    font-size: 4vw;
    font-weight: 400;
    @media(min-width: 480px) {
      font-size: 4.2vw;
    }
    @media(min-width: 768px) {
      font-size: 22px;
      text-align: left;
      margin-top: 60px;
    }
    @media(min-width: 992px) {
      font-size: 24px;
    }
    @media(min-width: 1200px) {
      font-size: 36px;
    }
    @media(min-width: 1430px) {
      font-size: 38px;
    }
  }
  // @media (min-width: 992px) {
  //   h1 {
  //     font-size: 50px;
  //   }
  //   h2 {
  //     font-size: 30px;
  //   }
  // }
  // @media (min-width: 1200px) {
  //   h1 {
  //     font-size: 65px;
  //   }
  //   h2 {
  //     font-size: 35px;
  //   }
  // }
  // @media (min-width: 1400px) {
  //   h1 {
  //     font-size: 75px;
  //   }
  // }
</style>
