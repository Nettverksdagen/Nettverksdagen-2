<template>
    <div class="sponsors mt-5">
      <Content>
        <h2 class="text-center font-weight-bold">Våre sponsorer</h2>
        <b-row>
          <Sponsor v-for="(sponsor, index) in sponsors"
                   :key="index"
                   :logo_src="sponsor.logo_uri"
                   :href="sponsor.website_url">
          </Sponsor>
        </b-row>
      </Content>
    </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import Sponsor from '@/components/anon/Sponsor.vue'
export default {
  name: 'Sponsors',
  components: { Content, Sponsor },
  data: function () {
    return {
      sponsors: []
    }
  },
  mounted: function () {
    this.$data.sponsors = this.$store.state.sponsors.all
  }
}
</script>

<style lang="scss" scoped>

</style>
