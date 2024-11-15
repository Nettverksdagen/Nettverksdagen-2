<template>
<<<<<<< HEAD
    <div class="about-view">
      <Content>
        <h1>{{$t('about') + ' ' + $t('nettverksdagene')}}</h1>
        <b-row>
          <b-col cols="12" lg="6">
            <p class="introduction">
              {{$t('nettis')}}
              <br>
              <br>
              {{$t('inntektene')}}
            </p>
          </b-col>
          <b-col cols="12" lg="6" class="d-block d-sm-block">
            <b-img class="image" src="@/assets/excited_people.jpg" fluid alt="Engasjerte studenter i Glassgården"/>
          </b-col>
        </b-row>
      </Content>
    </div>
=======
    <Content>
      <div>
        <!-- Render the quiz questions and results here -->
        <QuestionCard
          v-if="questions.length"
          :question="questions[currentQuestionIndex]"
          @answerSelected="handleAnswer"
        />
        <Result v-if="showResults" :topCompanies="topCompanies" />
        <ProgressBar :progress="progress" />
        <div class="navigation-buttons">
        <b-button @click="prevQuestion" :disabled="currentQuestionIndex === 0">Previous</b-button>
        </div>
      </div>
    </Content>
>>>>>>> 76bf235d9704a13872bd0f468b793b46626c01b6
  </template>
  
  <script>
  import Content from '@/components/common/Content.vue'
<<<<<<< HEAD
  export default {
    name: 'ValgomatView',
    components: {
      Content
    }
  }
=======
  import QuestionCard from '@/components/valgomat/QuestionCard.vue'
  import Result from '@/components/valgomat/Result.vue'
  import ProgressBar from '@/components/valgomat/ProgressBar.vue'

  export default {
    components: {
      Content,
      QuestionCard,
      Result,
      ProgressBar
    },
    data() {
      return {
        showResults: false,
        progress: 0,
        currentQuestionIndex: 0,
        topCompanies: [], // Stores top 3 companies based on the user's answers
        questions: [
          {
            id: 1,
            text: "What type of work environment do you prefer?",
            options: [
              { id: 1, text: "Collaborative", companyWeights: { CompanyA: 1, CompanyB: 2, CompanyC: 3 } },
              { id: 2, text: "Independent", companyWeights: { CompanyA: 3, CompanyB: 2, CompanyC: 1 } },
            ],
          },
          {
            id: 2,
            text: "What is your preferred programming language?",
            options: [
              { id: 1, text: "JavaScript", companyWeights: { CompanyA: 1, CompanyB: 2, CompanyC: 3 } },
              { id: 2, text: "Python", companyWeights: { CompanyA: 3, CompanyB: 2, CompanyC: 1 } },
            ],
          },
          {
            id: 3,
            text: "What is your preferred development methodology?",
            options: [
              { id: 1, text: "Agile", companyWeights: { CompanyA: 1, CompanyB: 2, CompanyC: 3 } },
              { id: 2, text: "Waterfall", companyWeights: { CompanyA: 3, CompanyB: 2, CompanyC: 1 } },
            ],
          },
        ],
        selectedAnswers: {}, // Stores the user's selected answers by question ID
      };
    },
    methods: {
      handleAnswer(questionId, option) {
        this.selectedAnswers[questionId] = option;
        this.calculateProgress();
        this.updateProgress();
        this.nextQuestion();
      },
      nextQuestion() {
        if (this.currentQuestionIndex < this.questions.length - 1) {
          this.currentQuestionIndex++;
        } else {
          this.showResults = true;
        }
      },
      prevQuestion() {
        if (this.currentQuestionIndex > 0) {
          this.currentQuestionIndex--;
        }
      },
      calculateScores() {
        const companyScores = {};
        for (const answer of Object.values(this.selectedAnswers)) {
          for (const [company, score] of Object.entries(answer.companyWeights)) {
            companyScores[company] = (companyScores[company] || 0) + score;
          }
        }
        //Sort and store the top 3 companies based on the scores
        this.topCompanies = Object.entries(companyScores)
          .sort(([, scoreA], [, scoreB]) => scoreB - scoreA)
          .slice(0, 3)
          .map(([company]) => company);
      },
      calculateProgress() {
        this.progress = (Object.keys(this.selectedAnswers).length / this.questions.length) * 100;
        if (this.progress === 100) this.showResults = true;
      },
      updateProgress() {
        this.progress = (Object.keys(this.selectedAnswers).length / this.questions.length) * 100;
        if (this.progress === 100) this.showResults = true;
      },
    },
  };
>>>>>>> 76bf235d9704a13872bd0f468b793b46626c01b6
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
<<<<<<< HEAD
      @media(min-width: 768px) {
        text-align: left;
      }
    }
    .image {
      border-style: solid;
      border: none;
      border-radius: 20px;
      overflow: hidden;
      margin-top: 20px;
      margin-bottom: 20px;
      @media(min-width: 768px) {
        margin-top: 0px;
      }
    }
    .about-view {
        min-height: 80vh;
=======
    }
    .navigation-buttons {
      display: flex;
      justify-content: space-between;
      margin-top: 20px;
>>>>>>> 76bf235d9704a13872bd0f468b793b46626c01b6
    }
  </style>
  