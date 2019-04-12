/**
 * Define all of your application routes here
 * for more information on routes, see the
 * official documentation https://router.vuejs.org/en/
 */

import EmptyPage from "../page/EmptyPage";
import UserHome from "../page/UserHome";

import LoginDialog from "../components/login/LoginDialog";
import InboundScan from "../components/inboundScan/InboundScan";
import Sorter from "../components/sorter/Sorter";
import Outbound from "../components/outbound/Outbound";

export default [
  {
    path: '/login',
    name: '',
    component: EmptyPage,
    children: [{
      path: '/',
      component: LoginDialog
    }]
  },
  {
    path: '/inbound-scan',
    name: '扫描入库',
    component: UserHome,
    children: [{
      path: '/',
      component: InboundScan
    }]
  },
  {
    path: '/sorter',
    name: '分拣',
    component: UserHome,
    children: [{
      path: '/',
      component: Sorter
    }]
  },
  {
    path: '/outbound',
    name: '播种合并',
    component: UserHome,
    children: [{
      path: '/',
      component: Outbound
    }]
  }
]
