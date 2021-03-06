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
import api from '../utils/api'

// Routes
import paths from './paths'

function route(path, name, page, component) {
  return {
    name: name,
    path,
    component: page,
    children: [{
      path: "/login",
      component: component
    }]
  }
}

Vue.use(Router)

// Create a new router
const router = new Router({
  //mode: 'history',
  //paths.map(path => route(path.path, path.name, path.page, path.component))
  routes: paths.concat([{
    path: '*',
    redirect: '/login'
  }]),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return {
        selector: to.hash
      }
    }
    return {
      x: 0,
      y: 0
    }
  }
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    api.checkLogin()
      .then(resp => {
        next();
      })
      .catch(resp => {
        next({
          path: '/login',
          query: {
            redirect: to.fullPath
          }
        });
      });
  } else {
    next() // make sure to always call next()!
  }
});

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