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
import { spinTheWheel } from './spinTheWheel.module'
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
    participant,
    spinTheWheel
  },
  plugins: [createPersistedState()]
})
