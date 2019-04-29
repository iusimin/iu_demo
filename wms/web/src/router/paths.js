/**
 * Define all of your application routes here
 * for more information on routes, see the
 * official documentation https://router.vuejs.org/en/
 */

import Empty from "@/wrapper/Empty";
import UserHome from "@/wrapper/UserHome";

import LoginDialog from "@/components/login/LoginDialog";
import HomeContent from "@/components/home/HomeContent";
import InboundScan from "@/components/inboundScan/InboundScan";
import Sorter from "@/components/sorter/Sorter";
import Outbound from "@/components/outbound/Outbound";
import Dashboard from "@/views/Dashboard.vue";
import WarehouseSetting from "@/components/admin/WarehouseSetting.vue";
import DirectShip from "@/components/operation/DirectShip.vue";
import OutboundScan from "@/components/operation/OutboundScan.vue";
import SortJob from "@/components/sorter/SortJob.vue";

export default [
  {
    path: '/login',
    name: 'login',
    component: Empty,
    children: [{
      path: '',
      component: LoginDialog
    }]
  },
  {
    path: '/home',
    name: 'dashboard',
    component: UserHome,
    children: [{
      path: 'dashboard',
      component: HomeContent
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/setting',
    name: 'warehousesetting',
    component: UserHome,
    children: [{
      path: 'warehouse-setting',
      component: WarehouseSetting
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/operation',
    name: '扫描入库',
    component: UserHome,
    children: [{
      path: 'inbound-scan',
      component: InboundScan,
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/operation',
    name: '分拣',
    component: UserHome,
    children: [{
      path: 'sorter',
      component: Sorter
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/operation',
    name: '播种合并',
    component: UserHome,
    children: [{
      path: 'seed',
      component: Outbound
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/operation',
    name: '直发打单',
    component: UserHome,
    children: [{
      path: 'directship',
      component: DirectShip
    }],
    meta: { requiresAuth: false }
  },
  {
    path: '/operation',
    name: '出库扫描',
    component: UserHome,
    children: [{
      path: 'outboundscan',
      component: OutboundScan
    }],
    meta: { requiresAuth: false }
  }
  ,
  {
    path: '/management',
    name: '分拣任务',
    component: UserHome,
    children: [{
      path: 'sort-job',
      component: SortJob
    }],
    meta: { requiresAuth: false }
  }
]
