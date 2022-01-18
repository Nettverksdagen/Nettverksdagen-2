import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '@/views/anon/HomeView'
import ListingsView from '@/views/anon/ListingsView'
import AnonBaseView from '@/views/anon/AnonBaseView'
import AdminBaseView from '@/views/admin/AdminBaseView'
import LoginView from '@/views/LoginView'
import AboutView from '@/views/anon/AboutView'
import ContactView from '@/views/anon/ContactView'
import ProgramView from '@/views/anon/ProgramView.vue'
import store from '../store/index.js'
import ListingAdminView from '@/views/admin/ListingAdminView.vue'
import BusinessAdminView from '@/views/admin/BusinessAdminView.vue'
import SponsorAdminView from '@/views/admin/SponsorAdminView.vue'
import TeamMemberAdminView from '@/views/admin/TeamMemberAdminView.vue'
import FormView from '@/views/anon/FormView'
import FormAdminView from '@/views/admin/FormAdminView.vue'
import BusinessDetails from '@/components/anon/BusinessDetails.vue'
import ListingDetails from '@/components/anon/ListingDetails.vue'
import ProgramAdminView from '@/views/admin/ProgramAdminView.vue'
import ParticipantAdminView from '@/views/admin/ParticipantAdminView.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: AnonBaseView,
      meta: {title: 'Nettverksdagen'},
      children: [
        {
          path: '',
          name: 'Home',
          component: HomeView,
          meta: {title: 'Nettverksdagen'},
          children: [
            {
              path: 'bedrift/:businessReferer',
              name: 'Business',
              component: BusinessDetails,
              meta: {title: 'Nettverksdagen'}
            }
          ]
        },
        {
          path: 'program',
          name: 'Program',
          component: ProgramView,
          meta: {title: 'Program'}
        },
        {
          path: 'stillinger',
          name: 'Listings',
          component: ListingsView,
          meta: {title: 'Stillingsannonser'},
          children: [
            {
              path: ':listingReferer',
              name: 'Listing',
              component: ListingDetails,
              meta: {title: 'Nettverksdagen'}
            }
          ]
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
        },
        {
          path: 'skjema/:form_internal_url',
          name: 'Form',
          component: FormView,
          meta: {title: 'Skjema'}
        }
      ]
    },
    {
      path: '/admin',
      component: AdminBaseView,
      beforeEnter: (to, from, next) => {
        if (store.state.admin.loggedIn) {
          next()
        } else {
          next({name: 'Login'})
        }
      },
      children: [
        {
          path: '',
          name: 'AdminOverview',
          component: null,
          meta: {title: 'Nvdagen admin'}
        },
        {
          path: 'stillinger',
          name: 'ListingAdmin',
          component: ListingAdminView,
          meta: {title: 'Rediger stillinger'}
        },
        {
          path: 'styret',
          name: 'TeamMemberAdmin',
          component: TeamMemberAdminView,
          meta: {title: 'Rediger styret'}
        },
        {
          path: 'bedrifter',
          name: 'CompanyAdmin',
          component: BusinessAdminView,
          meta: {title: 'Rediger Bedrifter'}
        },
        {
          path: 'sponsorer',
          name: 'SponsorAdmin',
          component: SponsorAdminView,
          meta: {title: 'Rediger sponsorer'}
        },
        {
          path: 'skjemaer',
          name: 'FormAdmin',
          component: FormAdminView,
          meta: {title: 'Rediger skjemaer'}
        },
        {
          path: 'program',
          name: 'ProgramAdmin',
          component: ProgramAdminView,
          meta: {title: 'Rediger program'}
        },
        {
          path: 'participant',
          name: 'ParticipantAdmin',
          component: ParticipantAdminView,
          meta: {title: 'Rediger deltagere'}
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      beforeEnter: (to, from, next) => {
        if (store.state.admin.loggedIn) {
          next({name: 'AdminOverview'})
        } else {
          next()
        }
      }
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    if (to.hash) {
      return {
        selector: to.hash,
        behavior: 'smooth'
      }
    }
    return { x: 0, y: 0 }
  }
})
