<template>
  <div>
    <FaqItem
      v-for="(faq, index) in faqs"
      :key="index"
      :question="faq.question"
      :answer="faq.answer"
    />
  </div>
</template>

<script>
// import { faqs } from "@/assets/FAQ_data";
import FaqItem from '@/components/anon/FaqItem.vue'

export default {
  name: 'FaqList',
  props: ['faqs'],
  components: {
    FaqItem
  }
}
</script>
