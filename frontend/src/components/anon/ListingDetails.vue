<template>
  <div class ="detailbox">
    <b-modal size="lg" @hide="hideModal" v-model="showModal" :id="'listingContent' + listing.id" :title="listing.name" hide-footer centered>
      <div class="listingText">
        <p v-html="listing.content"></p>
        <div class="button">
          <b-button :href="listing.listing_url" size="lg" variant="primary">{{$t('sokher')}}</b-button>
        </div>
      </div>
    </b-modal>
  </div>
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
    border: none;
    margin-left: 20px;
    margin-right: 20px;
    font-size: 18px;
    font-weight: 400;
    color: black;
  }
  .detailbox {
    border-radius: 15px;
    border: none;
  }
  /deep/ .modal-content {
    border: none;
    border-radius: 20px;
    background-color: var(--line-border-color);
    color: black;
    text-align: center;
  }
  /deep/ .modal-header {
    border-bottom: none;
  }
  /deep/ .modal-title {
    text-align: center;
    width: 100%;
  }
  /deep/ .btn-primary {
    color: #fff;
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    border-radius: 7px;
    margin-top: 5px;
  }
  .button {
    text-align: center;
    margin-bottom: 15px;
  }
  /deep/ h5 {
    margin-left: 20px;
    margin-top: 10px;
    margin-bottom: -10px;
    font-size: 26px;
  }
</style>
