<template>
  <div class="listings">
    <Content>
      <b-row>
        <div class="d-none d-md-block col-4">
          <b-card>
            <p>Her kommer det sortering</p>
          </b-card>
        </div>
        <div class="col-12 col-md-8">
          <b-list-group>
            <Listing v-for="listing in listings" :key="listing.id" :company="listing.company_name" :title="listing.name" deadline="20.10.2019"/>
          </b-list-group>
        </div>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import Listing from '@/components/anon/Listing.vue'
export default {
  name: 'Listings',
  components: {
    Content,
    Listing
  },
  computed: {
    listings: function () {
      return this.$store.state.listings.all
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
