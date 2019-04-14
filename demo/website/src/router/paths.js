/**
 * Define all of your application routes here
 * for more information on routes, see the
 * official documentation https://router.vuejs.org/en/
 */
export default [
  {
    path: '/home',
    name: 'Home',
    view: 'Home'
  },
  {
    path: '/signin',
    name: 'SignIn',
    view: 'login/SignIn'
  },
  {
    path: '/signup',
    name: 'SignUp',
    view: 'login/SignUp'
  },
  
  {
    path: '/user-profile',
    name: 'User Profile',
    view: 'rbac/UserProfile',
    meta: { loginRequired: true }
  },
  {
    path: '/demo',
    name: 'Demo',
    view: 'demo/Demo',
    meta: { loginRequired: true }
  },
  {
    path: '/users',
    name: 'Manage Users',
    view: 'rbac/ManageUsers',
    meta: { loginRequired: true }
  },
  {
    path: '/roles',
    name: 'Manage Roles',
    view: 'rbac/ManageRoles',
    meta: { loginRequired: true }
  },
  // Origin examples
  {
    path: '/typography',
    view: 'Typography'
  },
  {
    path: '/icons',
    view: 'Icons'
  },
  {
    path: '/maps',
    view: 'Maps'
  },
  {
    path: '/notifications',
    view: 'Notifications'
  },
  {
    path: '/upgrade',
    name: 'Upgrade to PRO',
    view: 'Upgrade'
  },
  {
    path: '/inbound-scan',
    name: '扫描入库',
    view: 'InboundScan/InboundScan'
  },
  {
    path: '/sorter',
    name: '分拣',
    view: 'Sorter/Sorter'
  },
  {
    path: '/outbound',
    name: '播种合并',
    view: 'Outbound/Outbound'
  }
]
