import { RouteRecordRaw } from 'vue-router';

export const projects: Array<RouteRecordRaw> = [
  {
    path: '/projects',
    name: 'projects',
    props: true,
    component: () => import('../pages/project/Projects.vue'),
  },
  {
    path: '/project-form',
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
        component: () => import('../pages/project/StatisticsPage.vue'),
      },
      {
        path: 'upload',
        name: 'upload',
        component: () => import('../pages/project/ItemsUpload.vue'),
      },
      {
        path: 'samples',
        name: 'samples',
        component: () => import('../pages/sample/Samples.vue'),
      },
      {
        path: 'experiments',
        name: 'experiments',
        component: () => import('../pages/experiment/Experiments.vue'),
      },
    ]
  }
]