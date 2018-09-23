<template>
  <div class="listing">
    <b-list-group-item class="inside">
      <div class="side logo-container">
        <img class="logo img-responsive center-block center" src="@/assets/logo.png">
      </div>
      <div class="side info-container">
        <h6 class="company">{{ company }}</h6>
        <h5 class="title">{{ title }}</h5>
        <span class="deadline">{{ deadline }}</span>
      </div>
    </b-list-group-item>
  </div>
</template>

<script>
export default {
  props: ['company', 'title', 'deadline']
}
</script>

<style lang="scss" scoped>
  .company, .title, .deadline {
    margin:0;
  }
  .inside {
    display:flex;
    flex-direction:row;
  }
  .logo-container {
    min-height:80px;
    min-width:80px;
    position:relative;
    margin-right:20px;
    flex-shrink:0;
  }
  .info-container {
    display:flex;
    flex-direction:column;
    justify-content: space-between;
    flex-shrink:2;
  }
  .logo {
    max-height:100%;
    max-width:100%;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
  }
  .company {
    font-weight:400;
    color:#333;
  }
  .title {
    /*@media (max-width:400px) {

    }*/
    font-weight:700;
  }
  .deadline {
    font-size:14px;
    color:#888;
  }
</style>
