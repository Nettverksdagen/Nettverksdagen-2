<template>
  <b-modal @hide="hideModal" v-model="showModal" :id="'businessText' + business.id" :title="business.name" hide-footer>
    <div class="businessText">
      <p>{{ business.text }}</p>
      <a :href="business.website_url" target="_blank" rel="noopener noreferrer">Gå til {{ business.name }} sin nettside</a>
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
</style>
