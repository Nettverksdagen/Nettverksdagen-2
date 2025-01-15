<template>
  <div id="appFAQ">
    <div class="content-wrapper">
      <div class="faq-container">
        <h1>{{$t('faq.header')}}</h1>
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
  padding: 0; /* Remove default padding */
}

.content-wrapper {
  display: flex;
  align-items: flex-start;
  width: 100%; /* Full screen width */
  padding: 20px;
  flex-direction: row; /* Default: items side by side */
}

.faq-container {
  flex: 3;
  margin-right: 20px; /* Space between FAQ and image */
}

/* Padding below header */
.faq-container h1 {
  margin-bottom: 30px; /* Adjust this value for more or less spacing */
}

.side-image {
  flex: 1;
  max-width: 600px;
  height: auto;
  border-radius: 10px;
  object-fit: cover;
  margin-right: 20px;
  margin-top: 80px;
}

/* Media query for smaller screens */
@media (max-width: 768px) { /* Adjust the width as needed for phones */
  .content-wrapper {
    flex-direction: column; /* Stack items vertically */
    align-items: center; /* Center content horizontally */
  }

  .faq-container {
    margin-right: 0; /* Remove right margin for vertical stacking */
  }

  .side-image {
    margin-top: 20px; /* Add spacing between content and image */
    margin-right: 0; /* Remove right margin for alignment */
  }
}
</style>
