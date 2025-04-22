import { RouteRecordRaw } from 'vue-router';


export const projectRoutes: Array<RouteRecordRaw> = [

  {
    name: 'project',
    path: '',
    props: true,
    component: () => import('../pages/ProjectDetails.vue'),
  },
  {
    path: ':modelName',
    props: true,
    component: () => import('../layouts/ModelLayout.vue'),
    children: [
      {
        path: '',
        name: 'details',
        props: true,
        component: () => import('../pages/ModelDetails.vue'),
      },
      {
        name: 'records',
        path: 'records',
        props: true,
        component: () => import('../pages/Records.vue')
      },
      {
        name: 'protocols',
        path: 'protocols',
        props: route => ({
          ...route.params,
          type: 'protocols'
        }), component: () => import('../pages/Links.vue')
      },
      {
        name: 'images',
        path: 'images',
        props: route => ({
          ...route.params,
          type: 'images'
        }), component: () => import('../pages/Links.vue')
      }
    ]
  }
]