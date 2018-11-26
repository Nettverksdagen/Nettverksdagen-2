<template>
    <div class="admin-base app">
      <Header>
        <SidebarToggler/>
      </Header>
        <div class="app-body">
          <main class="main">
            <div class="container-fluid">
              <router-view></router-view>
            </div>
          </main>
          <Sidebar>
            <SidebarNav :navItems="navItems">
            </SidebarNav>
          </Sidebar>
        </div>
    </div>
</template>

<script>
import { Header } from '@coreui/vue/src/components/Header'
import { Sidebar, SidebarNav, SidebarNavTitle, SidebarNavItem, SidebarNavLink, SidebarToggler } from '@coreui/vue/src/components/Sidebar'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faBars } from '@fortawesome/free-solid-svg-icons'
import axios from 'axios'
library.add(faBars)
export default {
  name: 'AdminBaseView',
  components: {
    Header,
    Sidebar,
    SidebarNav,
    SidebarNavTitle,
    SidebarNavItem,
    SidebarNavLink,
    SidebarToggler
  },
  computed: {
    navItems: function () {
      return [
        {
          title: 'Nvdagen admin',
          name: 'Nvdagen admin'
        },
        {
          name: 'Til hovedsiden',
          url: this.$router.resolve({name: 'Home'}).href,
          icon: 'cui-arrow-left'
        },
        {
          divider: true,
          class: 'sidebar-nav-divider'
        },
        {
          name: 'Oversikt',
          url: this.$router.resolve({name: 'AdminOverview'}).href,
          icon: 'cui-home'
        },
        {
          name: 'Stillingsannonser',
          url: this.$router.resolve({name: 'ListingAdmin'}).href,
          icon: 'cui-briefcase'
        },
        {
          name: 'Styremedlemmer',
          url: this.$router.resolve({name: 'BoardAdmin'}).href,
          icon: 'cui-people'
        },
        {
          name: 'Sponsorer',
          url: this.$router.resolve({name: 'SponsorAdmin'}).href,
          icon: 'cui-dollar'
        }
      ]
    }
  },
  mounted () {
    axios.defaults.headers.post['Authorization'] = 'Token ' + this.$store.state.admin.token
  }
}
</script>

<style lang="scss">
  @import '/frontend/node_modules/@coreui/icons/css/coreui-icons.min.css';
  @import '~@coreui/coreui/scss/coreui.scss';
  .sidebar-nav-divider {
    border-top: 1px solid rgba(0,0,0,0.2);
  }
</style>
