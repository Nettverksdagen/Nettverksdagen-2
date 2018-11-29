<template>
  <div class="business col-6 col-sm-4 col-md-3">
    <a :href="href">
      <b-img fluid :src="'http://127.0.0.1:9000/' + logo_src"></b-img>
    </a>
  </div>
</template>

<script>
export default {
  name: 'Business',
  props: ['logo_src', 'href']
}
</script>

<style lang="scss" scoped>
.business {
  transition:0.2s;
  padding: 5rem;
  &:hover {
    padding:4rem;
  }
}
</style>
