import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
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
  },
  {
    path: '/:projectId/samples',
    name: 'samples',
    component: () => import('../pages/sample/Samples.vue'),
    props: true
  },
  {
    path: '/:projectId/samples/form',
    name: 'sample-form',
    component: () => import('../pages/sample-form/SampleForm.vue'),
    props: true
  },
  {
    path: '/:projectId/samples/upload',
    name: 'sample-upload',
    component: () => import('../pages/sample-form/SamplesUpload.vue'),
    props: true
  },
  {
    name: 'experiments',
    path: '/:projectId/experiments',
    props: true,
    component: () => import('../pages/experiment/Experiments.vue'),
  },
  {
    name: 'sample',
    path: '/:projectId/samples/:sampleId',
    props: true,
    component: () => import('../pages/sample/Sample.vue')
  },
  {
    name: 'experiment',
    path: '/:projectId/experiments/:experimentId',
    props: true,
    component: () => import('../pages/experiment/Experiment.vue')
  },

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
