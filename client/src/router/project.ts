import { RouteRecordRaw } from 'vue-router';


export const projects: Array<RouteRecordRaw> = [
  {
    path: '/projects',
    name: 'projects',
    props: {
      title: 'Projects'
    },
    component: () => import('../pages/project/Projects.vue')
  },
  {
    path: '/projects/:projectId',
    props: true,
    name: 'project',
    component: () => import('../pages/project/Project.vue'),
  }
]