<template>
  <div class="listing">
    <b-link :href="listingUrl">
    <b-list-group-item class="inside p-4 listing-item">
      <div class="side logo-container">
        <img class="logo img-responsive center-block center" :src="logoSrc">
      </div>
      <div class="side info-container">
        <h6 class="company"><span class="font-weight-bold">{{ company }}</span> – {{ type }}</h6>
        <h5 class="title">{{ title }}</h5>
        <span class="deadline">Frist: {{ formattedDeadline }}</span>
      </div>
    </b-list-group-item>
    </b-link>
  </div>
</template>

<script>
export default {
  props: ['company', 'title', 'deadline', 'logoSrc', 'type', 'listingUrl'],
  computed: {
    formattedDeadline: function () {
      let deadDate = new Date(this.deadline)
      return deadDate.toLocaleDateString('no-NO', {
        year: 'numeric',
        day: 'numeric',
        month: 'short'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .listing-item:hover {
    background:#efefef;
    transition:0.1s;
  }
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
    margin-right:23px;
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
    color:#222;
  }
  .deadline {
    font-size:14px;
    color:#888;
  }
  a {
    text-decoration:none;
  }
</style>
