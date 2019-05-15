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

import axios from 'axios'
import login from '@/utils/login'
import rbac from '@/utils/rbac'

Vue.use(Router)

// Create a new router
const router = new Router({
  mode: 'history',
  routes: paths.map(p => {
    if (!p.children) {
      return p
    }
    if (!p.children.some(p => p.path == '')) {
      p.children = p.children.concat([{
        path: '',
        redirect: '/error/404'
      }])
    }
    if (!p.children.some(p => p.path == '*')) {
      p.children = p.children.concat([{
        path: '*',
        redirect: '/error/404'
      }])
    }
    return p
  }).concat([{
    path: '*',
    redirect: '/error/404'
  }]),
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
  axios.get(
    '/api/login',
    {}
  ).then(resp => {
    var data = resp.data
    console.log(data)
    if (!rbac.checkPermissions(data.permissions, to.meta.permissionRequired)) {
      next({
        path: '/error/401',
        query: {
          hint: 'You are not allowed to access this page.'
        }
      })
    }
    login.updateLoginStatus(data)
    if (to.matched.some(record => record.meta.loginRequired) && data.is_guest) {
      next({
        path: '/login/signin',
        query: {
          redirect: to.fullPath
        }
      })
    } else {
      next()
    }
  }).catch(error => {
    next({
      path: '/error/500'
    })
  })
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
