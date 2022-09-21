import Vue from 'vue'
import VueI18n from 'vue-i18n'
import nb from './nb.json'
import en from './en.json'

Vue.use(VueI18n)
const languages = {
  en: en,
  nb: nb
}

const messages = Object.assign(languages)

export const i18n = new VueI18n({
  locale: 'nb',
  fallbackLocale: 'nb',
  messages
})
