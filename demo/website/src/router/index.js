/**
 * Vue Router
 *
 * @library
 *
 * https://router.vuejs.org/en/
 */

// Lib imports
import Vue from 'vue'
import VueAnalytics from 'vue-analytics'
import Router from 'vue-router'
import Meta from 'vue-meta'

// Routes
import paths from './paths'

// Stores
import store from '@/store'

import axios from 'axios'
import login from '../utils/login'

function route (path, view, name, meta) {
  return {
    name: name || view,
    path,
    component: (resovle) => import(
      `@/views/${view}.vue`
    ).then(resovle),
    meta: meta
  }
}

Vue.use(Router)

// Create a new router
const router = new Router({
  mode: 'history',
  routes: paths.map(path => route(path.path, path.view, path.name, path.meta)).concat([
    { path: '*', redirect: '/home' }
  ]),
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { selector: to.hash }
    }
    return { x: 0, y: 0 }
  }
})

// Add login guard
router.beforeEach((to, from, next) => {
  // If login expired, check api and update
  if (login.loginExpired()) {
    axios.get(
      '/api/login',
      {}
    ).then(
      response => {
        var data = response.data
        login.updateLoginStatus(data)
        login.setLoginExpire()
        next()
      }
    ).catch(error => {
      // Also cache logged failed status
      login.setLoginExpire()
      if (to.meta.loginRequired) {
        // Redirect to sign in if require log in
        next({
          path: '/signin',
          query: {
            redirect: to.fullPath
          }
        })
      } else {
        next()
      }
    })
  } else {
    // Check cached result
    if (!to.meta.loginRequired || login.hasLoggedIn()) {
      next()
    } else {
      next({
        path: '/signin',
        query: {
          redirect: to.fullPath
        }
      })
    }
  }
})

Vue.use(Meta)

// Bootstrap Analytics
// Set in .env
// https://github.com/MatteoGabriele/vue-analytics
if (process.env.GOOGLE_ANALYTICS) {
  Vue.use(VueAnalytics, {
    id: process.env.GOOGLE_ANALYTICS,
    router,
    autoTracking: {
      page: process.env.NODE_ENV !== 'development'
    }
  })
}

export default router
