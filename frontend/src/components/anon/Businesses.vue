<template>
  <div class="businesses mt-5">
    <Content>
      <h2 class="text-center font-weight-bold">Bedrifter du kan møte på stand</h2>
      <div v-for="(level, index) in levels" :key="index">
        <b-row>
          <Business v-for="(business, index) in level.businesses"
                    :key="index"
                    :logo_src="business.logo_uri"
                    :href="business.website_url"
                    :text="business.text"
                    :id="business.id"
                    :name="business.name"
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
