import { RouteRecordRaw } from 'vue-router';
import { isAuthenticated, isAdmin } from './nav-guards'


export const adminRoutes: Array<RouteRecordRaw> = [
    {
        path: '/admin',
        name: 'admin',
        beforeEnter: [isAuthenticated, isAdmin],
        component: () => import('../layouts/RouterBypass.vue'),
        children: [
            {
                path: 'project-form',
                name: 'project-form',
                props: {
                    title: 'Project Form'
                },
                component: () => import('../pages/project-form/ProjectForm.vue')
            },
            {
                name: 'users',
                path: '/users',
                props: {
                    title: 'Users'
                },
                component: () => import('../pages/user/Users.vue')
            },
        ]
    }
]