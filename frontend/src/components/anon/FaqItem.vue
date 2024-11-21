<template>
  <div class="faq-item">
    <div class="question-section" @click="toggleAnswer">
      <h3>{{ question }}</h3>
    </div>
    <div v-if="showAnswer" class="answer-section">
      <p>{{ answer }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "FaqItem",
  props: {
    question: String,
    answer: String
  },
  data() {
    return {
      showAnswer: false
    };
  },
  methods: {
    toggleAnswer() {
      this.showAnswer = !this.showAnswer;
    }
  }
};
</script>

<style scoped>
.faq-item {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 15px;
  transition: box-shadow 0.3s ease;
  cursor: pointer;
}

.faq-item:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.question-section h3 {
  margin: 0;
  color: #14403c;
  font-weight: bold;
}

.question-section {
  padding-bottom: 8px;
  border-bottom: 2px solid #14403c;
}

.answer-section {
  margin-top: 10px;
  color: #333333;
  line-height: 1.5;
}
</style>
