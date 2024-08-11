import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { projects } from './project'
import Dashboard from '../pages/dashboard/Dashboard.vue'



const routes: Array<RouteRecordRaw> = [
  {
    name: 'home',
    path: '/',
    component: Dashboard,
    meta: {
      layout: 'default',
    },
  },
  {
    name: 'login',
    path: '/login',
    component: () => import('../pages/auth/login/Login.vue'),
    meta: {
      layout: 'default',
    },
  },
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'home' },
  },
  ...projects
]



const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_PATH ? import.meta.env.VITE_BASE_PATH : import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
