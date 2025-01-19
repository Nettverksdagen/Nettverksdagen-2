<template>
  <div id="appFAQ">
    <Content>
      <h1 class="page-header">{{$t('faq.header')}}</h1>
      <b-row>
        <b-col cols="12" lg="6">
          <FaqList :faqs="$t('faq.questions')" />
        </b-col>
        <b-col cols="12" lg="6" class="d-block d-sm-block">
          <b-img src="@/assets/NVDBilde2.jpg" fluid alt="Related image" class="side-image"/>
        </b-col>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import FaqList from '@/components/anon/FaqList.vue'

export default {
  name: 'FAQView',
  components: {
    Content,
    FaqList
  }
}
</script>

<style scoped lang="scss">
  #appFAQ {
    flex: 1;
  }

  .side-image {
    border-radius: 20px;
  }
</style>
