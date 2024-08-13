import { RouteRecordRaw } from 'vue-router';
import { useGlobalStore } from '../stores/global-store'

function isAdmin() {
    const { userRole } = useGlobalStore()
    if (userRole !== 'Admin') {
      return { name: 'unauthorized' }
    }
  }
  
  function isAuthenticated() {
    const { isAuthenticated } = useGlobalStore()
    if (!isAuthenticated) return { name: 'login' }
  }
  
export const projects: Array<RouteRecordRaw> = [
  {
    path: '/projects',
    name: 'projects',
    props: true,
    component: () => import('../pages/project/Projects.vue'),
    meta: {
      layout: 'default',
    },
  },
  {
    path: '/project-form',
    name: 'project-form',
    component: () => import('../pages/project-form/ProjectForm.vue'),
    meta: {
      layout: 'default',
    },
  },
  {
    path: '/projects/:projectId',
    props: true,
    component: () => import('../pages/project/Project.vue'),
    meta: {
      layout: 'project',
    },
    children: [
      {
        path: '',
        name: 'project',
        component: () => import('../pages/project/Overview.vue')
      },
      {
        path: 'statistics',
        name: 'statistics',
        component: () => import('../pages/project/StatisticsPage.vue'),
      },
      {
        path: 'upload',
        name: 'upload',
        component: () => import('../pages/project/Upload.vue'),
      },
      {
        path: 'samples',
        name: 'samples',
        component: () => import('../pages/project/Samples.vue'),
      },
      {
        path: 'experiments',
        name: 'experiments',
        component: () => import('../pages/project/Experiments.vue'),
      },
    ]
  }
]