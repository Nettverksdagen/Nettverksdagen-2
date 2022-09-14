import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const messages = {
  'nb': {
    lang: 'English',
    stillingsannonser: 'Stillingsannonser',
    kontakt: 'Kontakt',
    omoss: 'Om oss',
    fremtidig: 'Møt din fremtidige arbeidsgiver på',
    program22: 'Slik så programmet for Nettverksdagene 2022 ut:',
    hensikt: 'Nettverksdagene er en karrieremesse arrangert av studenter på studiet Kybernetikk og robotikk ved NTNU. Hensikten er å gi studentene mulighet til å møte sine fremtidige arbeidsgivere, få informasjon om sommerjobber og et innblikk i arbeidslivet.'
  },
  'en': {
    lang: 'Norsk',
    stillingsannonser: 'Job advertisements',
    kontakt: 'Contact',
    omoss: 'About us',
    fremtidig: 'Meet your future employer at',
    program22: 'This was the program for Nettverksdagene 2022:',
    hensikt: 'Nettverksdagene is a ...'
  }
}

export const i18n = new VueI18n({
  locale: 'nb',
  fallbackLocale: 'nb',
  messages
})
