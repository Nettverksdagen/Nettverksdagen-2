<template>
  <div class="anon-header">
    <div class="content">
      <b-link :to="'/'" class="logo-link">
        <div class="side">
          <img class="logo" src="@/assets/logo.png">
          <h1>Nettverksdagen</h1>
        </div>
      </b-link>
      <div class="side">
        <b-nav class="links">
          <b-nav-item :to="{name: 'Home'}" active>Hjem</b-nav-item>
          <b-nav-item :to="{name: 'Program'}">Program</b-nav-item>
          <b-nav-item :to="{name: 'Listings'}">Stillinger</b-nav-item>
          <b-nav-item :to="{name: 'About'}">Om oss</b-nav-item>
          <b-nav-item :to="{name: 'Contact'}">Kontakt</b-nav-item>
          <b-nav-item href="https://blogg.nvdagen.no">Blogg</b-nav-item>
       </b-nav>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .anon-header {
    background-color:#fff;
  }
  h1 {
    display:inline;
    margin:0;
    padding:0;
    border:0;
    color:#444;
    font-size:20px;
    white-space:nowrap;
    @media (min-width: 768px) {
      font-size:22px;
    }
    @media (min-width: 992px) {
      font-size:30px;
    }
    @media (min-width: 1400px) {
      font-size:40px;
    }
  }
  .logo {
    height:40px;
    margin:5px 11px;
    @media (min-width: 992px) {
      margin:15px 15px 15px 0;
      height:50px;
    }
    @media (min-width: 1400px) {
      margin:20px 20px 20px 0;
      height:60px;
    }
  }
  .logo-link {
    text-decoration:none !important;
  }
  .content {
    display:flex;
    flex-direction: row;
    justify-content: space-between;
    align-content:stretch;
    flex-wrap: nowrap;
    margin: 0 15px;
    @media (min-width: 1200px) {
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
    a {
      color:#444;
      &:hover {
        color:#111;
      }
    }
  }
  @media (max-width: 767px) {
    .logo-link {
      position:relative;
      left:50%;
      margin-left:-110px;
    }
  }
</style>
