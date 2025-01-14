<template>
  <b-modal @hide="hideModal" v-model="showModal" :id="'businessText' + business.id" :title="business.name" hide-footer centered>
    <div class="businessText">
      <p v-html="business.text"></p>
      <div class="button">
          <b-button :href="business.website_url" target="_blank" rel="noopener noreferrer" size="lg" variant="primary">Besøk {{ business.name }} sin nettside</b-button>
      </div>
    </div>
    <b-img fluid :src="fileserverHost + '/thumb/512/' + business.logo_uri"></b-img>
  </b-modal>
</template>

<script>
export default {
  name: 'BusinessDetails',
  data () {
    return {
      fileserverHost: process.env.VUE_APP_FILESERVER_HOST,
      showModal: this.businesses !== false
    }
  },
  methods: {
    hideModal () {
      this.$router.push('/')
    }
  },
  computed: {
    business: function () {
      let businesses = this.$store.state.businesses.all
      for (let i = 0; i < businesses.length; i++) {
        if (businesses[i].name.replace(/\s+/g, '-').toLowerCase() === this.$route.params.businessReferer) {
          return businesses[i]
        }
      }
      return false
    }
  }
}
</script>

<style lang="scss" scoped>
  .businessText {
    white-space: pre-line;
  }
    ::v-deep .modal-content {
    border: none;
    border-radius: 20px;
    background-color: var(--line-border-color);
    color: black;
    text-align: center;
  }
  ::v-deep .modal-header {
    border-bottom: none;
  }
  ::v-deep .modal-title {
    text-align: center;
    width: 100%;
  }
  ::v-deep .btn-primary {
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
  ::v-deep h5 {
    margin-left: 20px;
    margin-top: 10px;
    margin-bottom: -10px;
    font-size: 26px;
  }
</style>
