import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
  },
  {
    path: '/setup',
    name: 'Setup',
    component: () => import('../views/auth/Setup.vue'),
  },
  {
    path: '/',
    component: () => import('../components/layout/AppLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '仪表盘' },
      },
      {
        path: 'devices',
        name: 'DeviceList',
        component: () => import('../views/devices/DeviceList.vue'),
        meta: { title: '设备列表' },
      },
      {
        path: 'devices/:id',
        name: 'DeviceDetail',
        component: () => import('../views/devices/DeviceDetail.vue'),
        meta: { title: '设备详情' },
      },
      {
        path: 'scanning',
        name: 'ScanTasks',
        component: () => import('../views/devices/ScanTasks.vue'),
        meta: { title: '扫描任务' },
      },
      {
        path: 'inspection',
        name: 'InspectionManage',
        component: () => import('../views/devices/InspectionManage.vue'),
        meta: { title: '巡检管理' },
      },
      {
        path: 'alive',
        name: 'AliveDetection',
        component: () => import('../views/devices/AliveDetection.vue'),
        meta: { title: '存活检测' },
      },
      {
        path: 'history',
        name: 'ExecutionHistory',
        component: () => import('../views/devices/ExecutionHistory.vue'),
        meta: { title: '执行记录' },
      },
      {
        path: 'instant',
        name: 'InstantLogin',
        component: () => import('../views/instant/InstantLogin.vue'),
        meta: { title: '即时登录' },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('../views/settings/Settings.vue'),
        meta: { title: '系统设置' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.path !== '/login' && to.path !== '/setup' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
