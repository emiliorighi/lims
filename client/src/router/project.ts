import { RouteRecordRaw } from 'vue-router';

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
      name: 'project',
      props: true,
      component: () => import('../pages/project/Project.vue'),
    }  
  ]