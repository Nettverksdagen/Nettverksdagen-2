<template>
  <div class="form-view">
    <Content>
      <b-row>
        <iframe
          v-if="form"
          v-bind:src="form.external_url"
          v-bind:height="form.iframe_height"
          width="100%"
          frameborder="0" marginheight="0" marginwidth="0">{{$t('loadingmsg')}}</iframe>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
export default {
  name: 'FormView',
  components: {
    Content
  },
  computed: {
    form: function () {
      let internalUrl = this.$route.params.form_internal_url
      return this.$store.getters['forms/form'](internalUrl)
    }
  }
}
</script>

<style lang="scss" scoped>
  .form-view {
      min-height: 80vh;
  }
</style>
