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
          url: '/',
          icon: 'cui-arrow-left'
        },
        {
          divider: true,
          class: 'sidebar-nav-divider'
        },
        {
          name: 'Oversikt',
          url: '/admin',
          icon: 'cui-home'
        },
        {
          name: 'Stillingsannonser',
          url: '/admin/stillinger',
          icon: 'cui-briefcase'
        },
        {
          name: 'Styremedlemmer',
          url: '/admin/styret',
          icon: 'cui-people'
        },
        {
          name: 'Sponsorer',
          url: '/admin/sponsorer',
          icon: 'cui-dollar'
        }
      ]
    }
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
