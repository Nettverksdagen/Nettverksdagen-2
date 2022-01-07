<template>
    <div class="row col-12" align="center">
    <div class="sponsor col-3">
      <a :href="href" target="_blank" rel="noopener noreferrer">
        <b-img fluid :src="fileserverHost + '/thumb/512/' + logo_src"></b-img>
      </a>
    </div>
    </div>
</template>

<script>
export default {
  name: 'Sponsor',
  props: ['logo_src', 'href'],
  data () {
    return {
      fileserverHost: process.env.VUE_APP_FILESERVER_HOST
    }
  }
}
</script>

<style lang="scss" scoped>
  .allsponsors {
    position:relative;
    //width:80%;
    left:10%;
  }
  .sponsor {
    width: 200px;
    //width: 80%;
    //display:flex;
    //flex-direction:row;
    //justify-content: space-between;
    //width: 10%;
    transition: transform 300ms, filter 500ms;
    filter: brightness(0) invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(94%) contrast(94%);
    //padding: 0.5rem 1.5rem;
  }
  .sponsor:hover {
    filter: none;
    transform: scale(1.15);
    transition: filter 0.5s, transform 0.3s;
  }
</style>
