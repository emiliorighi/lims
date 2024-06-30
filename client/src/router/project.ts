import { RouteRecordRaw } from 'vue-router';
import { samples } from './sample';
import { experiments } from './experiment';
export const projects: Array<RouteRecordRaw> = [
  {
    path: '/projects',
    name: 'projects',
    props: true,
    component: () => import('../pages/project/Projects.vue'),
  },
  {
    path: '/projects/project-form',
    name: 'project-form',
    component: () => import('../pages/project-form/ProjectForm.vue'),
  },
  {
    path: '/projects/:projectId',
    props: true,
    component: () => import('../pages/project/Project.vue'),
    children: [
      {
        path: '',
        name: 'project',
        component: () => import('../pages/project/components/Details.vue')
      },
      {
        path: 'statistics',
        name: 'statistics',
        props: true,
        component: () => import('../pages/project/StatisticsPage.vue'),
      },
      {
        path: 'upload',
        name: 'upload',
        props: true,
        component: () => import('../pages/project/ItemsUpload.vue'),
      },
      ...samples,
      ...experiments
    ]
  }
]