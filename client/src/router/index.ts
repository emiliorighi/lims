import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { isAuthenticated, isAdmin } from './nav-guards'
import { projectRoutes } from './project'
import { authRoutes } from './auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'home' },
  },
  
  {
    path: '/',
    component: () => import('../layouts/AppLayout.vue'),
    children:[
      {
        path: '',
        name: 'home',
        component: () => import('../pages/Dashboard.vue'),
      },
      {
        path: '/docs',
        name: 'docs',
        component: () => import('../pages/Documentation.vue'),
      },
      {
        name: 'users',
        path: '/users',
        beforeEnter: [isAuthenticated, isAdmin],
        component: () => import('../pages/Users.vue')
      },
      {
        path: '/project-form',
        name: 'project-form',
        beforeEnter: [isAuthenticated, isAdmin],
        component: () => import('../pages/ProjectForm.vue')
      },
      {
        path: '/projects',
        name: 'projects',
        component: () => import('../pages/Projects.vue')
      },
      ...authRoutes,
    ]
  },
  {
    path: '/projects/:projectId',
    props:true,
    component: () => import('../layouts/ProjectLayout.vue'),
    children:[
      ...projectRoutes
    ]
  },

]


const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_PATH ? import.meta.env.VITE_BASE_PATH : import.meta.env.BASE_URL),
  routes
})

export default router
