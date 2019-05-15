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
          v-for="(link, i) in visiableLinks"
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

import Base from '@/mixins/Base.vue'
import rbac from '@/utils/rbac'

export default {
  mixins: [Base],
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
        visible: true
      },
      {
        to: '/rbac/users',
        icon: 'mdi-view-dashboard',
        text: 'Manage User',
        visible: true
      },
      {
        to: '/rbac/roles',
        icon: 'mdi-view-dashboard',
        text: 'Manage Role & Permission',
        visible: true
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
    },
    visiableLinks () {
      return this.links.filter(l => l.visible)
    }
  },
  watch: {
    loginPermissions (p) {
      this.renderLinks(p)
    }
  },
  mounted () {
    this.renderLinks(this.loginPermissions)
    this.onResponsiveInverted()
    window.addEventListener('resize', this.onResponsiveInverted)
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
    renderLinks (p) {
      for (let link of this.links) {
        link.visible = rbac.canAccessPage(link.to, this.$router)
      }
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
