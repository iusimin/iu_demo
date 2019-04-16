/**
 * Define all of your application routes here
 * for more information on routes, see the
 * official documentation https://router.vuejs.org/en/
 */

import EmptyPage from "@/page/EmptyPage";
import UserHome from "@/page/UserHome";

import LoginDialog from "@/components/login/LoginDialog";
import HomeContent from "@/components/home/HomeContent";
import InboundScan from "@/components/inboundScan/InboundScan";
import Sorter from "@/components/sorter/Sorter";
import Outbound from "@/components/outbound/Outbound";
import Dashboard from "@/views/Dashboard.vue";

export default [
  {
    path: '/login',
    name: 'login',
    component: EmptyPage,
    children: [{
      path: '/',
      component: LoginDialog
    }]
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: UserHome,
    children: [{
      path: '/',
      component: HomeContent,
      meta: { requiresAuth: true }
    }],
    meta: { requiresAuth: true }
  },
  {
    path: '/inbound-scan',
    name: '扫描入库',
    component: UserHome,
    children: [{
      path: '/',
      component: InboundScan,
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/sorter',
    name: '分拣',
    component: UserHome,
    children: [{
      path: '/',
      component: Sorter
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/outbound',
    name: '播种合并',
    component: UserHome,
    children: [{
      path: '/',
      component: Outbound
    }],
    meta: { requiresAuth: true }
  }
]
