<template>
  <div class="question-card">
    <!-- question title -->
    <h2>{{ $t(question.text_key) }}</h2>

    <!-- options -->
    <ul>
      <li v-for="option in question.options" :key="option.id" class="option" @click="$emit('answerSelected', question.id, option)">
        {{ $t(option.text_key) }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    question: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.question-card {
  border: 1px solid #ddd;
  padding: 40px;
  margin: 10px 0;
  border-radius: 4px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
.option {
  cursor: pointer;
  padding: 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}
.option:hover {
  background-color: #f0f0f0;
}
</style>
