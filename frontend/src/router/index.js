import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Listings from '@/components/Listings'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {title: 'Nettverksdagen'}
    },
    {
      path: '/stillinger',
      name: 'Listings',
      component: Listings,
      meta: {title: 'Stillingsannonser'}
    }
  ]
})
