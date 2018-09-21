<template>
  <div class="header">
    <div class="content">
      <div class="side">
        <img class="logo" src="@/assets/logo.png">
        <h1>Nettverksdagen</h1>
      </div>
      <div class="side">
        <b-nav class="links">
          <b-nav-item active>Hjem</b-nav-item>
          <b-nav-item>Program</b-nav-item>
          <b-nav-item>Stillinger</b-nav-item>
          <b-nav-item>Om oss</b-nav-item>
       </b-nav>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .header {
  }
  h1 {
    display:inline;
    margin:0;
    padding:0;
    border:0;
    color:#444;
    font-size:22px;
    white-space:nowrap;
    @media (min-width: 992px) {
      font-size:30px;
    }
    @media (min-width: 1400px) {
      font-size:40px;
    }
  }
  .logo {
    height:50px;
    margin:0 11px;
    @media (min-width: 992px) {
      margin:20px;
      height:75px;
    }
    @media (min-width: 1400px) {
      margin:30px;
      height:80px;
    }
  }
  .content {
    display:flex;
    flex-direction: row;
    justify-content: space-between;
    align-content:stretch;
    flex-wrap: nowrap;
    margin: 0 15px;
    @media (min-width: 992px) {
      margin: 0 100px;
    }
    @media (min-width: 1400px) {
      margin: 0 200px;
    }
  }
  .side {
    align-items: center;
    display:flex;
  }
  .links {
    display:none;
    @media (min-width: 768px) {
      display:flex;
    }
    @media (min-width: 992px) {
      display:flex;
      font-size:20px;
    }
    @media (min-width: 1400px) {
      font-size:26px;
    }
    a {
      color:#444;
      &:hover {
        color:#111;
      }
    }
  }
</style>
