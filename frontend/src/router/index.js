import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '@/views/anon/HomeView'
import ListingsView from '@/views/anon/ListingsView'
import AnonBaseView from '@/views/anon/AnonBaseView'
import AdminBaseView from '@/views/admin/AdminBaseView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Base',
      component: AnonBaseView,
      meta: {title: 'Nettverksdagen'},
      children: [
        {
          path: '',
          name: 'Home',
          component: HomeView,
          meta: {title: 'Nettverksdagen'}
        },
        {
          path: 'stillinger',
          name: 'Listings',
          component: ListingsView,
          meta: {title: 'Stillingsannonser'}
        }
      ]
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminBaseView
    }
  ]
})
