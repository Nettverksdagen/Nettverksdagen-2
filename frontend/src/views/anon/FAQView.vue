<template>
  <div id="appFAQ">
    <div class="content-wrapper">
      <div class="faq-container">
        <h1 class="page-header">{{$t('faq.header')}}</h1>
        <FaqList :faqs="$t('faq.questions')" />
      </div>
      <img src="@/assets/NVDBilde2.jpg" alt="Related image" class="side-image" />
    </div>
  </div>
</template>

<script>
import FaqList from '@/components/anon/FaqList.vue'

export default {
  name: 'FAQView',
  components: {
    FaqList
  }
}
</script>

<style scoped>
#appFAQ {
  font-family: Arial, sans-serif;
  padding: 0;
}

.content-wrapper {
  display: flex;
  align-items: flex-start;
  width: 100%;
  padding: 20px;
  flex-direction: row; /* Default layout: side by side */
}

.faq-container {
  flex: 3;
  margin-right: 20px; /* Space between FAQ and image */
}

.faq-container h1 {
  margin-bottom: 30px;
}

.side-image {
  flex: 1;
  max-width: 600px;
  height: auto;
  border-radius: 10px;
  object-fit: cover;
  margin-top: 80px; /* Default spacing above image */
}

@media (max-width: 1000px) {
  .content-wrapper {
    flex-direction: column;
    align-items: center;
  }

  .faq-container {
    margin-right: 0;
  }

  .side-image {
    margin-top: 20px;
    margin-right: 0;
  }
}
</style>

