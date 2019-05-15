/**
 * Define all of your application routes here
 * for more information on routes, see the
 * official documentation https://router.vuejs.org/en/
 */

import UserHome from '@/wrapper/UserHome.vue'
import Empty from '@/wrapper/Empty.vue'

export default [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/error/:code',
    name: 'error',
    component: Empty,
    children: [{
      path: '',
      component: () => import('@/components/common/ErrorPage.vue')
    }]
  },
  {
    path: '/home',
    name: 'Home',
    component: UserHome,
    children: [{
      path: '',
      component: () => import('@/components/common/WelcomePage.vue')
    }]
  },
  {
    path: '/login',
    name: 'Login',
    component: Empty,
    children: [{
      path: 'signin',
      component: () => import('@/components/login/SignIn.vue')
    }, {
      path: 'signup',
        component: () => import('@/components/login/SignUp.vue')
    }]
  },
  {
    path: '/demo',
    name: 'Demo',
    component: UserHome,
    children: [{
      path: '',
      component: () => import('@/components/demo/Demo.vue'),
      meta: {
        loginRequired: true
      }
    }]
  },
  {
    path: '/rbac',
    name: 'RBAC',
    component: UserHome,
    children: [{
      path: 'roles',
      component: () => import('@/components/rbac/ManageRoles.vue'),
      meta: {
        loginRequired: true,
        permissionRequired: [
          {
            'resource': '/api/roles/',
            'actions': ['GET', 'POST', 'PUT', 'DELETE']
          },
          {
            'resource': '/api/role/',
            'actions': ['GET', 'POST', 'PUT', 'DELETE']
          }
        ]
      }
    }, {
      path: 'users',
        component: () => import('@/components/rbac/ManageUsers.vue'),
    }]
  }
]
