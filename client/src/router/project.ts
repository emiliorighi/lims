import { RouteRecordRaw, RouteLocationNormalizedLoaded } from 'vue-router';
import { useGlobalStore } from '../stores/global-store'
import { useSchemaStore } from '../stores/schemas-store';
import { title } from 'process';



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
    props: {
      title: 'Projects'
    },
    component: () => import('../pages/project/Projects.vue'),
    meta: {
      layout: 'default',
    },
  },
  {
    path: '/project-form',
    name: 'project-form',
    props: {
      title: 'Project Form'
    },
    component: () => import('../pages/project-form/ProjectForm.vue'),
    meta: {
      layout: 'default',
    },
  },
  {
    path: '/projects/:projectId',
    props: true,
    component: () => import('../layouts/ProjectBypass.vue'),
    meta: {
      layout: 'project',
    },
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
        props: { model: 'sample', title: 'Samples', icon: 'fa-vial', buttonLabel: 'Add Sample' },
        component: () => import('../pages/project/children/Items.vue'),
      },
      {
        path: 'experiments',
        name: 'experiments',
        props: { model: 'experiment', title: 'Experiments', icon: 'fa-dna', buttonLabel: 'Add Experiment' },
        component: () => import('../pages/project/children/Items.vue'),
      },
    ]
  }
]