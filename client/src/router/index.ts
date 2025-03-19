import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { isAuthenticated, isAdmin } from './nav-guards'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'home' },
  },
  {
    path: '/',
    component: () => import('../layouts/AppLayout.vue'),
    children: [
      {
        name: 'home',
        path: '',
        component: () => import('../pages/dashboard/Dashboard.vue'),
        props: {
          title: 'Dashboard'
        }
      },
      {
        name: 'docs',
        path: 'docs',
        component: () => import('../pages/docs/Documentation.vue'),
      },
      {
        name: 'login',
        path: 'login',
        props: {
          title: 'Login'
        },
        component: () => import('../pages/auth/Login.vue')
      },
      {
        name: 'unauthorized',
        path: 'unauthorized',
        props: {
          title: 'You are unauthorized'
        },
        component: () => import('../pages/auth/Unauthorized.vue')
      },
      {
        path: 'projects',
        name: 'projects',
        props: {
          title: 'Projects'
        },
        component: () => import('../pages/project/Projects.vue')
      },
      {
        name: 'users',
        path: '/users',
        beforeEnter: [isAuthenticated, isAdmin],
        props: {
          title: 'Users'
        },
        component: () => import('../pages/user/Users.vue')
      },
      {
        path: '/project-form',
        name: 'project-form',
        beforeEnter: [isAuthenticated, isAdmin],
        props: {
          title: 'Create Project'
        },
        component: () => import('../pages/research-project-form/ResearchProjectForm.vue')
      },
    ]
  },
  {
    path: '/projects/:projectId',
    props: true,
    name: 'project',
    component: () => import('../layouts/ProjectLayout.vue'),
    children: [
      {
        name: 'projectSchema',
        path: '',
        props: true,
        component: () => import('../pages/project/Project.vue')
      },
      {
        name: 'projectModel',
        path: ':modelName',
        props: true,
        component: () => import('../pages/project/Model.vue')
      },
      {
        name: 'modelForm',
        path: 'model-form',
        props: true,
        component: () => import('../pages/project/ModelForm.vue')
      },
      {
        name: 'uploadData',
        path: 'upload-form',
        props: true,
        component: () => import('../pages/project/UploadForm.vue')
      },
    ]
  },

]


const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_PATH ? import.meta.env.VITE_BASE_PATH : import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
