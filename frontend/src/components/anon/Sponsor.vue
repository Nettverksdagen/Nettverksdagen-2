<template>
    <div class="sponsor col-6 col-sm-4 col-md-3">
      <a :href="href">
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
    transition:0.2s;
    padding: 4rem;
    @media(min-width: 576px) {
      // No hover effect on tiny devices
      padding: 5rem;
    }
    @media(min-width: 768px) {
      padding: 5rem;
      &:hover {
        padding: 4rem;
      }
    }
    @media(min-width: 992px) {
      padding: 6rem;
      &:hover {
        padding: 5rem;
      }
    }
    @media(min-width: 1200px) {
      padding: 7rem;
      &:hover {
        padding: 6rem;
      }
    }
    &:hover {
      padding:6rem;
    }
  }
</style>
