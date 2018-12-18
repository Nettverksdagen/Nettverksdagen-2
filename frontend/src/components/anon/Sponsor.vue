<template>
    <div class="sponsor col-6 col-sm-4 col-md-3">
      <a :href="href">
        <b-img fluid :src="'http://127.0.0.1:9000/' + logo_src"></b-img>
      </a>
    </div>
</template>

<script>
export default {
  name: 'Sponsor',
  props: ['logo_src', 'href']
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
