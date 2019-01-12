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
    transition: transform 0.2s;
    padding: 0.5rem 2rem;
    @media(min-width: 576px) {
      // No hover effect on tiny devices
      padding: 0.5rem 3rem;
    }
    @media(min-width: 768px) {
      padding: 2rem 4rem;
      &:hover {
        transform: scale(1.15);
      }
    }
    @media(min-width: 992px) {
      padding: 2rem 5.5rem;
    }
  }
</style>
