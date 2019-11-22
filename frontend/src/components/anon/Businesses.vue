<template>
  <div class="businesses mt-5">
    <Content>
      <div v-for="(level, index) in levels" :key="index">
        <h2 class="text-center font-weight-bold">{{ levels[index].levelHeader }}</h2>
        <b-row class="justify-content-center">
          <Business v-for="(business, index) in level.businesses"
                    :key="index"
                    :logo_src="business.logo_uri"
                    :href="business.website_url"
                    :colSize="$options.sizes[business.level]">
          </Business>
        </b-row>
        <hr>
      </div>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import Business from '@/components/anon/Business.vue'
export default {
  name: 'Businesses',
  components: { Content, Business },
  data: function () {
    return {
      businesses: []
    }
  },
  mounted: function () {
    this.$data.businesses = this.$store.state.businesses.all
  },
  computed: {
    levels: function () {
      return this.$store.getters['businesses/levels']
    }
  },
  sizes: {
    'Hovedsamarbeidspartner': 'big',
    'Samarbeidspartner': 'big',
    'Gull': 'big',
    'Sølv': 'medium',
    'Bronse': 'small'
  }
}
</script>

<style lang="scss" scoped>
  h2 {
    font-size: 2.5rem;
  }
</style>
