import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import RouterBypass from '../layouts/RouterBypass.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/projects',
    component: RouterBypass,
    children: [
      {
        path: '',
        name: 'projects',
        props: true,
        component: () => import('../pages/project/Projects.vue'),
      },
      {
        name: 'project-form',
        path: 'project-form',
        component: () => import('../pages/project/ProjectForm.vue'),
      },
      {
        path: ':projectId',
        name: 'project',
        props: true,
        component: () => import('../pages/project/Project.vue'),
        children: [
          {
            path: 'samples',
            component: RouterBypass,
            children: [
              {
                name: 'samples',
                path: '',
                props: true,
                component: () => import('../pages/sample/Samples.vue')
              },
              {
                name: 'sample',
                path: ':sampleId',
                props: true,
                component: () => import('../pages/sample/Sample.vue')
              },
            ]
          },
          {
            path: 'experiments',
            component: RouterBypass,
            children: [
              {
                name: 'experiments',
                path: '',
                props: true,
                component: () => import('../pages/experiment/Experiments.vue'),
              },
              {
                name: 'experiment',
                path: ':experimentId',
                props: true,
                component: () => import('../pages/experiment/Experiment.vue')
              },
            ]
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
