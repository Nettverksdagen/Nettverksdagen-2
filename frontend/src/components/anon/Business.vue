<template>
  <div class="business col-6 col-sm-4 col-md-3">
    <a :href="href">
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
  transition:0.2s;
  padding: 1rem;
  @media(min-width: 576px) {
    // No hover effect on tiny devices
    padding: 2rem;
  }
  @media(min-width: 768px) {
    padding: 3rem;
    &:hover {
      padding: 2rem;
    }
  }
  @media(min-width: 992px) {
    padding: 4rem;
    &:hover {
      padding: 3rem;
    }
  }
  @media(min-width: 1200px) {
    padding: 5rem;
    &:hover {
      padding: 4rem;
    }
  }
  &:hover {
    padding:4rem;
  }
}
</style>
