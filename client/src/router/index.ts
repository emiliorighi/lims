import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { projects } from './project'
import Dashboard from '../pages/dashboard/Dashboard.vue'



const routes: Array<RouteRecordRaw> = [
  {
    name: 'home',
    path: '/',
    component: Dashboard
  },
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'home' },
  },
  ...projects
]



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
