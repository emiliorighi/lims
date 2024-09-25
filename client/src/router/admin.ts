import { RouteRecordRaw } from 'vue-router';
import { isAuthenticated, isAdmin } from './nav-guards'


export const adminRoutes: Array<RouteRecordRaw> = [
    {
        name: 'users',
        path: '/users',
        beforeEnter: [isAuthenticated, isAdmin],
        props: {
            title: 'Users'
        },
        component: () => import('../pages/user/Users.vue')
    },
    {
        path: '/project-form',
        name: 'project-form',
        beforeEnter: [isAuthenticated, isAdmin],
        props: {
            title: 'Project Form'
        },
        component: () => import('../pages/project-form/ProjectForm.vue')
    },
]