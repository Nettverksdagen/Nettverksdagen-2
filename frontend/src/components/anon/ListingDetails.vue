<template>
    <b-modal size="lg" @hide="hideModal" v-model="showModal" :id="'listingContent' + listing.id" :title="listing.name" hide-footer>
      <div class="listingText">
        <p v-html="listing.content"></p>
        <a :href="listing.listing_url">Søk her</a>
      </div>
    </b-modal>
</template>

<script>
export default {
  name: 'ListingDetails',
  data () {
    return {
      fileserverHost: process.env.VUE_APP_FILESERVER_HOST,
      showModal: true
    }
  },
  methods: {
    hideModal () {
      this.$router.push('/stillinger')
    },
    formatDeadline: function (deadline) {
      let deadDate = new Date(deadline)
      return deadDate.toLocaleDateString('no-NO', {
        year: 'numeric',
        day: 'numeric',
        month: 'short'
      })
    }
  },
  computed: {
    listing: function () {
      let listings = this.$store.state.listings.all
      for (let i = 0; i < listings.length; i++) {
        if (listings[i].internal_url === this.$route.params.listingReferer) {
          return listings[i]
        }
      }
      return false
    }
  }
}
</script>

<style lang="scss" scoped>
  .listingText {
    white-space: pre-line;
  }
</style>
