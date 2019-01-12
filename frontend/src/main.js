// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import store from './store'
import 'es6-promise/auto'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'babel-polyfill'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(BootstrapVue)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store: store,
  data () {
    return {
      info: null
    }
  },
  mounted () {
    this.fetchListings()
    this.fetchBusinesses()
    this.fetchSponsors()
    this.fetchTeamMembers()
  },
  methods: {
    ...Vuex.mapActions('listings', ['fetchListings']),
    ...Vuex.mapActions('businesses', ['fetchBusinesses']),
    ...Vuex.mapActions('sponsors', ['fetchSponsors']),
    ...Vuex.mapActions('teamMembers', ['fetchTeamMembers'])
  },
  components: { App },
  template: '<App/>'
})
