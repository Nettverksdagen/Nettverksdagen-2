<template>
  <div>
    <QuestionCard
      v-if="questions.length && !showResults"
      :question="questions[currentQuestionIndex]"
      @answerSelected="handleAnswer"
    />
    <div v-if="showResults">
      <h1>{{$t('valgomatresulttitle')}}</h1>
      <p>{{$t('valgomatresulttext')}}</p>
      <ul>
        <li v-for="company in topCompanies" :key="company">
          <h2>{{ companyDescription[company][0] }}</h2>
          <p>{{ companyDescription[company][1] }}</p>
        </li>
      </ul>
    </div>
    <ProgressBar :progress="progress" />
    <div v-if="!showResults" class="navigation-buttons">
      <b-button @click="prevQuestion" :disabled="currentQuestionIndex === 0">Previous</b-button>
    </div>
  </div>
</template>
  
<script>
import QuestionCard from '@/components/valgomat/QuestionCard.vue'
import ProgressBar from '@/components/valgomat/ProgressBar.vue'
import questions from '@/components/valgomat/questions.json';
import companyDescription from '@/components/valgomat/companyDescription.json'

export default {
  components: {
    QuestionCard,
    ProgressBar
  },
  data() {
    return {
      showResults: false,
      progress: 0,
      currentQuestionIndex: 0,
      topCompanies: [], // Stores top 3 companies based on the user's answers
      companyDescription: companyDescription,
      questions,
      selectedAnswers: {}, // Stores the user's selected answers by question ID
    };
  },
  methods: {
    handleAnswer(questionId, option) {
      this.selectedAnswers[questionId] = option;
      this.calculateProgress();
      this.nextQuestion();
    },
    nextQuestion() {
      this.currentQuestionIndex++;
      this.calculateProgress();
      if (this.currentQuestionIndex === this.questions.length) {
        this.calculateScores();
        this.showResults = true;
      }
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
        this.calculateProgress();
      }
    },
    calculateScores() {
      const companyScores = {}
      for (const question of this.questions) {
        const answer = this.selectedAnswers[question.id]
        if (answer) {
          for (const [company, score] of Object.entries(answer.companyWeights)) {
            companyScores[company] = (companyScores[company] || 0) + score
          }
        }
      }
      this.topCompanies = Object.entries(companyScores)
        .sort(([, scoreA], [, scoreB]) => scoreB - scoreA)
        .slice(0, Math.min(3, Object.keys(companyScores).length))
        .map(([company]) => company)
    },
    calculateProgress() {
      this.progress = this.currentQuestionIndex / this.questions.length * 100
    }
  }
}
</script>

<style lang="scss" scoped>
.introduction {
  font-size:18px;
  text-align: center;
  @media(min-width: 768px) {
    text-align: left;
    margin-right: 30px;
  }
}
h1 {
  font-size: 36px;
  font-weight: 600;
  text-align: center;
  color: black;
  margin-bottom: 30px;
  margin-top: 40px;
}
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>
