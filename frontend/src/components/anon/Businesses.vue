<template>
  <div class="businesses mt-5">
    <Content>
      <h1 class="text-center font-weight-bold">Bedrifter du kan møte på stand</h1>
      <b-row>
          <Business v-for="(business, index) in businesses"
                    :key="index"
                    :logo_src="business.logo_uri"
                    :href="business.website_url">
          </Business>
      </b-row>
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
  }
}
</script>

<style lang="scss" scoped>

</style>
