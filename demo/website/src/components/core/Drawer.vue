<template>
  <v-navigation-drawer
    id="app-drawer"
    v-model="inputValue"
    app
    dark
    floating
    persistent
    mobile-break-point="991"
    width="260"
  >
    <v-img
      :src="image"
      height="100%"
    >
      <v-layout
        class="fill-height"
        tag="v-list"
        column
      >
        <v-list-tile avatar>
          <v-list-tile-avatar
            color="white"
          >
            <v-img
              :src="logo"
              height="34"
              contain
            />
          </v-list-tile-avatar>
          <v-list-tile-title class="title">
            {{ loginUsername || 'Guest' }}
          </v-list-tile-title>
        </v-list-tile>
        <v-divider/>
        <v-list-tile
          v-if="responsive"
        >
          <v-text-field
            class="purple-input search-input"
            label="Search..."
            color="purple"
          />
        </v-list-tile>
        <v-list-tile
          v-for="(link, i) in links"
          v-if="link.visible"
          :key="i"
          :to="link.to"
          :active-class="color"
          avatar
          class="v-list-item"
        >
          <v-list-tile-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-title
            v-text="link.text"
          />
        </v-list-tile>
        <v-list-tile
          disabled
          active-class="primary"
          class="v-list-item v-list__tile--buy"
          to="/upgrade"
        >
          <v-list-tile-action>
            <v-icon>mdi-package-up</v-icon>
          </v-list-tile-action>
          <v-list-tile-title class="font-weight-light">
            Upgrade To PRO
          </v-list-tile-title>
        </v-list-tile>
      </v-layout>
    </v-img>
  </v-navigation-drawer>
</template>

<script>
// Utilities
import {
  mapMutations,
  mapState
} from 'vuex'
import Login from '../mixins/Login.vue'

export default {
  mixins: [Login],
  data: () => ({
    logo: './img/vuetifylogo.png',
    links: [
      {
        to: '/home',
        icon: 'mdi-view-dashboard',
        text: 'Home',
        visible: true
      },
      {
        to: '/demo',
        icon: 'mdi-view-dashboard',
        text: 'Demo',
        login_display: true,
        visible: false
      },
      {
        to: '/users',
        icon: 'mdi-view-dashboard',
        text: 'Manage User',
        login_display: true,
        permission_display: '/api/users',
        visible: false
      },
      {
        to: '/roles',
        icon: 'mdi-view-dashboard',
        text: 'Manage Role & Permission',
        login_display: true,
        permission_display: '/api/roles',
        visible: false
      }
    ],
    responsive: false
  }),
  computed: {
    ...mapState('app', ['image', 'color']),
    inputValue: {
      get () {
        return this.$store.state.app.drawer
      },
      set (val) {
        this.setDrawer(val)
      }
    },
    items () {
      return this.$t('Layout.View.items')
    }
  },
  watch: {
    loginPermissions: function (p) {
      for (let i in this.links) {
        var link = this.links[i]
        this.links[i].visible = this.hasPermission(
          link.login_display, link.permission_display
        )
      }
    }
  },
  mounted () {
    this.onResponsiveInverted()
    window.addEventListener('resize', this.onResponsiveInverted)
    this.updateLoginStatus()
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.onResponsiveInverted)
  },
  methods: {
    ...mapMutations('app', ['setDrawer', 'toggleDrawer']),
    onResponsiveInverted () {
      if (window.innerWidth < 991) {
        this.responsive = true
      } else {
        this.responsive = false
      }
    },
    hasPermission (requireLogin, requirePermission) {
      if (!requireLogin && !requirePermission) {
        return true
      }
      if (!requirePermission && requireLogin && this.loginUserId) {
        return true
      }
      if (requirePermission) {
        for (let i in this.loginPermissions) {
          var permission = this.loginPermissions[i]
          var regex = new RegExp(permission.resource)
          if (regex.test(requirePermission)) {
            return permission.allow
          }
        }
      }
      return false
    }
  }
}
</script>

<style lang="scss">
  #app-drawer {
    .v-list__tile {
      border-radius: 4px;

      &--buy {
        margin-top: auto;
        margin-bottom: 17px;
      }
    }

    .v-image__image--contain {
      top: 9px;
      height: 60%;
    }

    .search-input {
      margin-bottom: 30px !important;
      padding-left: 15px;
      padding-right: 15px;
    }
  }
</style>
