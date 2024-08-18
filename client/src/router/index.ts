import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { projects } from './project'
import { adminRoutes } from './admin'
import Dashboard from '../pages/dashboard/Dashboard.vue'

const routes: Array<RouteRecordRaw> = [
  {
    name: 'home',
    path: '/',
    component: Dashboard,
    props: {
      title: 'Dashboard'
    }
  },
  {
    name: 'login',
    path: '/login',
    props: {
      title: 'Login'
    },
    component: () => import('../pages/auth/Login.vue')
  },
  {
    name: 'unauthorized',
    path: '/unauthorized',
    props: {
      title: 'You are unauthorized'
    },
    component: () => import('../pages/auth/Unauthorized.vue')
  },
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'home' },
  },
  ...projects,
  ...adminRoutes
]


const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_PATH ? import.meta.env.VITE_BASE_PATH : import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
