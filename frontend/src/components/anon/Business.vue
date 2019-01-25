<template>
  <b-col
    :cols="$options.colSizes[colSize][0]"
    :sm="$options.colSizes[colSize][1]"
    :md="$options.colSizes[colSize][2]"
    :class="'business ' + colSize">
    <a :href="href" target="_blank" rel="noopener noreferrer">
      <b-img fluid :src="fileserverHost + '/thumb/512/' + logo_src"></b-img>
    </a>
  </b-col>
</template>

<script>
export default {
  name: 'Business',
  props: ['logo_src', 'href', 'colSize'],
  data () {
    return {
      fileserverHost: process.env.VUE_APP_FILESERVER_HOST
    }
  },
  colSizes: {
    'big': [6, 4, 4],
    'medium': [4, 3, 3],
    'small': [3, 2, 2]
  }
}
</script>

<style lang="scss" scoped>
  .business {
    transition: transform 0.2s;

    @media(min-width: 768px) {
      &:hover {
        transform: scale(1.15);
      }
    }
    &.big {
      padding: 0.5rem 2rem;
      @media(min-width: 576px) {
        padding: 2rem;
      }
      @media(min-width: 768px) {
        padding: 1rem 2rem;
      }
      @media(min-width: 992px) {
        padding: 0.5rem 5.5rem;
      }
    }

    &.medium {
      padding: 1.5rem;
      @media(min-width: 576px) {
        padding: 1.5rem;
      }
      @media(min-width: 768px) {
        padding: 1.5rem 2.5rem;
      }
      @media(min-width: 992px) {
        padding: 1.5rem 5rem;
      }
    }

    &.small {
      padding: 1.2rem;
      @media(min-width: 576px) {
        padding: 1rem;
      }
      @media(min-width: 768px) {
        padding: 2rem 2rem;
      }
      @media(min-width: 992px) {
        padding: 1.5rem 3.25rem;
      }
    }
  }
</style>
