import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '@/views/anon/HomeView'
import ListingsView from '@/views/anon/ListingsView'
import AnonBaseView from '@/views/anon/AnonBaseView'
import AdminBaseView from '@/views/admin/AdminBaseView'
import LoginView from '@/views/LoginView'
import AboutView from '@/views/anon/AboutView'
import ContactView from '@/views/anon/ContactView'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
        },
        {
          path: 'om',
          name: 'About',
          component: AboutView,
          meta: {title: 'Om oss'}
        },
        {
          path: 'kontakt',
          name: 'Contact',
          component: ContactView,
          meta: {title: 'Kontakt oss'}
        }
      ]
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminBaseView,
      children: [
        {
          path: 'stillinger',
          name: 'ListingAdmin',
          component: null,
          meta: {title: 'Rediger stillinger'}
        },
        {
          path: 'styret',
          name: 'BoardAdmin',
          component: null,
          meta: {title: 'Rediger styret'}
        },
        {
          path: 'sponsorer',
          name: 'SponsorAdmin',
          component: null,
          meta: {title: 'Rediger sponsorer'}
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    }
  ]
})
