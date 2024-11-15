<template>
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
  </template>
  
  <script>
  import Content from '@/components/common/Content.vue'
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
            text: "Hvilket fagområde interesserer deg mest?",
            options: [
              { id: 1, text: "Teknologi og innovasjon", companyWeights: { Thelma_Biotel: 1, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 0, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 1, Eltorque: 1, Nemko: 1, ABB: 1 } },
              { id: 2, text: "Miljø og bærekraft", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 1, Element_Logic: 1, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 1, Nemko: 1, ABB: 1 } },
              { id: 3, text: "Helse og biomedision", companyWeights: { Thelma_Biotel: 1, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 0 } },
              { id: 4, text: "Energi og fornybare ressurser", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 1 } },
              { id: 5, text: "Annet", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 1, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 0 } },
            ],
          },
          {
            id: 2,
            text: "Hvor ønsker du å jobbe?",
            options: [
              { id: 1, text: "Kan jobbe hvor som helst", companyWeights: { Thelma_Biotel: 1, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 1, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 1, Eltorque: 1, Nemko: 1, ABB: 1 } },
              { id: 2, text: "Oslo", companyWeights: { Thelma_Biotel: 0, Cisco: 1, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 3, text: "Trondheim", companyWeights: { Thelma_Biotel: 1, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 1, Nemko: 0, ABB: 1 } },
              { id: 4, text: "Stavanger", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 1 } },
              { id: 5, text: "Bergen", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 1 } },
              { id: 6, text: "Nord-Norge", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 7, text: "Midt-Norge", companyWeights: { Thelma_Biotel: 1, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 1, Nemko: 0, ABB: 0 } },
              { id: 8, text: "Sørlandet", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 1, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 1, Eltorque: 0, Nemko: 1, ABB: 0 } },
              { id: 9, text: "Østlandet", companyWeights: { Thelma_Biotel: 0, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 10, text: "Vestlandet", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 1, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 11, text: "Utenlands", companyWeights: { Thelma_Biotel: 0, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 0, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 1, Nemko: 1, ABB: 1 } },
            ],
          },
          {
            id: 3,
            text: "Hva er viktigst for deg på en arbeidsplass?",
            options: [
              { id: 1, text: "Godt arbeidsmiljø og sosiale tiltak", companyWeights: { Thelma_Biotel: 0, Cisco: 1, Brunvoll: 0, Element_Logic: 1, NFEA: 0, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 0 } },
              { id: 2, text: "Høy lønn", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 1, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 3, text: "Fleksible arbeidstider", companyWeights: { Thelma_Biotel: 1, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 1, Eltorque: 1, Nemko: 0, ABB: 0 } },
              { id: 4, text: "Muligheter for faglig utvikling", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 1, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 0 } },
              { id: 5, text: "Bærekraftige og miljønevennlige løsninger", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 1, Applica_Consulting: 0, Eltorque: 1, Nemko: 0, ABB: 1 } },
            ],
          },
          {
            id: 4,
            text: "Hvordan fortrekker du å jobbe?",
            options: [
              { id: 1, text: "I åpent kontorlandskap", companyWeights: { Thelma_Biotel: 0, Cisco: 1, Brunvoll: 0, Element_Logic: 1, NFEA: 0, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 2, text: "Selvstendig på eget kontor", companyWeights: { Thelma_Biotel: 1, Cisco: 0, Brunvoll: 1, Element_Logic: 0, NFEA: 1, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 1, Eltorque: 1, Nemko: 0, ABB: 0 } },
              { id: 3, text: "Hjemmekontor", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 0 } },
            ],
          },
          {
            id: 5,
            text: "Hva slags bedrift ønsker du å jobbe i?",
            options: [
              { id: 1, text: "Startup", companyWeights: { Thelma_Biotel: 1, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 0, Eltorque: 1, Nemko: 0, ABB: 0 } },
              { id: 2, text: "Stor og etablert bedrift", companyWeights: { Thelma_Biotel: 0, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 1, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 3, text: "Nøytral", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 1, Applica_Consulting: 1, Eltorque: 0, Nemko: 0, ABB: 0 } },
            ],
          },
          {
            id: 6,
            text: "Hvilken rolle ser du for deg i fremtiden?",
            options: [
              { id: 1, text: "Konsulent", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 1, Eltorque: 0, Nemko: 0, ABB: 0 } },
              { id: 2, text: "Leder", companyWeights: { Thelma_Biotel: 1, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 1, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 1, Eltorque: 1, Nemko: 1, ABB: 1 } },
              { id: 3, text: "Ingeniør i fast konsern", companyWeights: { Thelma_Biotel: 1, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 1, Sopra_Steria: 0, Fugro: 1, Applica_Consulting: 0, Eltorque: 1, Nemko: 1, ABB: 1 } },
              { id: 4, text: "Nøytral", companyWeights: { Thelma_Biotel: 1, Cisco: 1, Brunvoll: 1, Element_Logic: 1, NFEA: 1, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 1, Eltorque: 1, Nemko: 1, ABB: 1 } },
            ],
          },
          {
            id: 7,
            text: "Hvor viktig er følgende for deg?",
            options: [
              { id: 1, text: "Sosiale tiltak som ping-pong og kaffemaskin", companyWeights: { Thelma_Biotel: 0, Cisco: 1, Brunvoll: 0, Element_Logic: 1, NFEA: 0, Sopra_Steria: 1, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 0 } },
              { id: 2, text: "Lønn", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 1, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 0, Eltorque: 0, Nemko: 1, ABB: 1 } },
              { id: 3, text: "Fleksible arbeidstider", companyWeights: { Thelma_Biotel: 1, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 0, Sopra_Steria: 0, Fugro: 0, Applica_Consulting: 1, Eltorque: 1, Nemko: 0, ABB: 0 } },
              { id: 4, text: "Jobbe med bærekraft", companyWeights: { Thelma_Biotel: 0, Cisco: 0, Brunvoll: 0, Element_Logic: 0, NFEA: 1, Sopra_Steria: 1, Fugro: 1, Applica_Consulting: 0, Eltorque: 0, Nemko: 0, ABB: 0 } },
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
  