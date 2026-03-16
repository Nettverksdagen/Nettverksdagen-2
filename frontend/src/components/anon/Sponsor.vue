<template>
    <div class="sponsor col-3">
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
    margin: auto;
    transition: transform 0.2s;
    padding: 1rem 1rem;
      @media(min-width: 576px) {
        padding: 0rem 3rem;
      }
      @media(min-width: 1200px) {
        padding: 0.5rem 5.25rem;
      }
  }
  .sponsor:hover {
    @media(min-width: 768px) {
      transform: scale(1.15);
    }
  }
</style>
