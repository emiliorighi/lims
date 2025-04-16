import { RouteRecordRaw } from 'vue-router';

export const authRoutes:Array<RouteRecordRaw> = [

    {
        name: 'login',
        path: '/login',
        props: {
          title: 'Login'
        },
        component: () => import('../pages/Login.vue')
      },
      {
        name: 'unauthorized',
        path: '/unauthorized',
        props: {
          title: 'You are unauthorized'
        },
        component: () => import('../pages/Unauthorized.vue')
      },
]