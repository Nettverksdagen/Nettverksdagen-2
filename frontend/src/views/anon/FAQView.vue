<template>
  <div id="appFAQ">
    <Content>
      <h1 class="page-header">{{$t('faq.header')}}</h1>
      <b-row>
        <b-col cols="12" lg="6">
          <FaqList :faqs="displayFaqs" />
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
import { mapState } from 'vuex'

export default {
  name: 'FAQView',
  components: {
    Content,
    FaqList
  },
  computed: {
    ...mapState('faq', ['all']),
    displayFaqs() {
      const lang = this.$i18n.locale
      return this.all.map(faq => ({
        question: lang === 'en' ? faq.question_en : faq.question_nb,
        answer: lang === 'en' ? faq.answer_en : faq.answer_nb
      }))
    }
  },
  created() {
    // Fetch FAQs from API when component is created
    this.$store.dispatch('faq/fetchFAQs')
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