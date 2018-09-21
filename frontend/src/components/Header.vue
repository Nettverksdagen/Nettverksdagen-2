<template>
  <div class="header ">
    <div class="content">
      <div class="side">
        <img class="logo" src="@/assets/logo.png">
        <h1>Nettverksdagen</h1>
      </div>
      <div class="side">
        <b-nav>
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
    color:#555;
    font-size:22px;
    white-space:nowrap;
    @media (min-width: 768px) {
      font-size:30px;
    }
    @media (min-width: 1200px) {
      font-size:40px;
    }
  }
  .logo {
    height:50px;
    margin:0 11px;
    @media (min-width: 768px) {
      margin:20px;
      height:75px;
    }
    @media (min-width: 1200px) {
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
    margin: 15px 15px;
    @media (min-width: 768px) {
      margin: 0 100px;
    }
    @media (min-width: 1200px) {
      margin: 0 200px;
    }
  }
  .side {
    align-items: center;
    display:flex;
  }
</style>
