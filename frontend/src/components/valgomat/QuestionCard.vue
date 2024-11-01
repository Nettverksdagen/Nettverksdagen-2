<template>
    <div class="question-card">
      <h2>{{ question.text }}</h2>
      <ul>
        <li
          v-for="option in question.options"
          :key="option.id"
          @click="selectOption(option)"
          class="option"
        >
          {{ option.text }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      question: {
        type: Object,
        required: true,
      },
    },
    methods: {
      selectOption(option) {
        // Emit the selected option back to the parent
        this.$emit('answerSelected', this.question.id, option);
      },
    },
  };
  </script>
  
  <style scoped>
  .question-card {
    border: 1px solid #ddd;
    padding: 20px;
    margin: 10px 0;
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
  