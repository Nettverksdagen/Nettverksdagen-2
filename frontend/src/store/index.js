import Vue from 'vue'
import Vuex from 'vuex'
import { listings } from './listings.module'
import { admin } from './admin.module'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)
export default new Vuex.Store({
  modules: {
    listings,
    admin
  },
  plugins: [createPersistedState()]
})
