import { RouteRecordRaw } from 'vue-router';

export const projects: Array<RouteRecordRaw> = [
    {
      path: '/',
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
      path: '/:projectId',
      name: 'project',
      props: true,
      component: () => import('../pages/project/Project.vue'),
    }  
  ]