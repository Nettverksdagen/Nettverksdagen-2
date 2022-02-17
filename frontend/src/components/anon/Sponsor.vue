<template>
    <div class="sponsor col-4 col-md-3">
      <a :href="href" target="_blank" rel="noopener noreferrer">
        <b-img fluid :src="fileserverHost + '/thumb/512/' + logo_src"></b-img>
      </a>
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
  .sponsor {
    position: relative;
    justify-content: space-between;
    margin: auto;
    margin-bottom: 30px;
    transition: transform 300ms, filter 500ms;
    transform: scale(0.7);
    // filter: brightness(0) invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(94%) contrast(94%);
    // @media(min-width: 768px) {
    //   transform: scale(0.8);
    // }
    // @media(min-width: 1200px) {
    //   transform: scale(1.6);
    // }
  }
  .sponsor:hover {
    transition: filter 0.5s, transform 0.3s;
    @media(min-width: 1200px) {
      filter: none;
    }
  }
</style>
