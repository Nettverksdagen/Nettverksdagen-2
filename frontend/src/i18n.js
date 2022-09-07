import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.useAttrs(VueI18n);

const messages = {
    'nb': {
        overskrift: "Møt fremtidige arbeidsgivere på"
    },
    'en': {
        overskrift: "Meet your future employers during"
    }
};

const i18n = new VueI18n({
    locale: 'nb',
    fallbackLocale: 'en',
    messages,
});