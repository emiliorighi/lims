import { RouteRecordRaw } from 'vue-router';
import { hasProjectAccess, isAuthenticated } from './nav-guards'


export const projects: Array<RouteRecordRaw> = [
  {
    path: '/projects',
    name: 'projects',
    // beforeEnter: [isAuthenticated],
    props: {
      title: 'Projects'
    },
    component: () => import('../pages/project/Projects.vue')
  },
  {
    path: '/projects/:projectId',
    props: true,
    // beforeEnter: [isAuthenticated, hasProjectAccess],
    component: () => import('../layouts/ProjectBypass.vue'),
    children: [
      {
        path: '',
        name: 'project',
        props: {
          title: 'Overview'
        },
        component: () => import('../pages/project/children/Overview.vue')
      },
      {
        path: 'statistics',
        name: 'statistics',
        props: {
          title: 'Statistics'
        },
        component: () => import('../pages/project/children/Statistics.vue'),
      },
      {
        path: 'upload',
        name: 'upload',
        props: {
          title: 'Upload'
        },
        component: () => import('../pages/project/children/Upload.vue'),
      },
      {
        path: 'samples',
        name: 'samples',
        props: { model: 'sample', title: 'Samples', icon: 'fa-vial', buttonLabel: 'Sample' },
        component: () => import('../pages/project/children/Items.vue'),
      },
      {
        path: 'experiments',
        name: 'experiments',
        props: { model: 'experiment', title: 'Experiments', icon: 'fa-dna', buttonLabel: 'Experiment' },
        component: () => import('../pages/project/children/Items.vue'),
      },
    ]
  }
]