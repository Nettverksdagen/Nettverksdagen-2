<template>
  <div class="business col-6 col-sm-4 col-md-3">
    <a :href="href" target="_blank" rel="noopener noreferrer">
      <b-img fluid :src="fileserverHost + '/thumb/512/' + logo_src"></b-img>
    </a>
  </div>
</template>

<script>
export default {
  name: 'Business',
  props: ['logo_src', 'href'],
  data () {
    return {
      fileserverHost: process.env.VUE_APP_FILESERVER_HOST
    }
  }
}
</script>

<style lang="scss" scoped>
  .business {
    transition: transform 0.2s;
    padding: 2rem;
    @media(min-width: 576px) {
      // No hover effect on tiny devices
      padding: 2rem;
    }
    @media(min-width: 768px) {
      padding: 2rem 2.5rem;
      &:hover {
        transform: scale(1.2);
      }
    }
    @media(min-width: 992px) {
      padding: 1.5rem 3.5rem;
    }
  }
</style>
