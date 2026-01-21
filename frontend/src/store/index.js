import Vue from 'vue'
import Vuex from 'vuex'
import { listings } from './listings.module'
import { businesses } from './businesses.module'
import { sponsors } from './sponsors.module'
import { admin } from './admin.module'
import { teamMembers } from './teamMembers.module'
import { forms } from './forms.module'
import { program } from './program.module'
import { participant } from './participant.module'
<<<<<<< HEAD
import { infobox } from './infobox.module'
||||||| parent of 624049c (feat: fix frontend for FAQ admin view and refactor FAQ to read from db)
=======
import { faq } from './faq.module'
>>>>>>> 624049c (feat: fix frontend for FAQ admin view and refactor FAQ to read from db)
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)
export default new Vuex.Store({
  modules: {
    listings,
    businesses,
    sponsors,
    admin,
    teamMembers,
    forms,
    program,
<<<<<<< HEAD
    participant,
    infobox
||||||| parent of 624049c (feat: fix frontend for FAQ admin view and refactor FAQ to read from db)
    participant
=======
    participant,
    faq
>>>>>>> 624049c (feat: fix frontend for FAQ admin view and refactor FAQ to read from db)
  },
  plugins: [createPersistedState()]
})
