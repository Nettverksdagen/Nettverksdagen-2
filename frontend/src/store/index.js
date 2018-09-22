import Vue from 'vue'
import Vuex from 'vuex'

import { listings } from './listings.module'
Vue.use(Vuex)
export default new Vuex.Store({
  modules: {
    listings
  }
})
