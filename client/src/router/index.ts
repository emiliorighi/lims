import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { experiments } from './experiment'
import { samples } from './sample'
import { projects } from './project'

const routes: Array<RouteRecordRaw> = [
  ...projects,
  ...samples,
  ...experiments
]



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
