import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import AppLayout from '../layouts/AppLayout.vue'

import RouteViewComponent from '../layouts/RouterBypass.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'dashboard' },
  },
  // {
  //   name: 'projects',
  //   path: '/projects',
  //   component: () => import('../pages/project/Projects.vue'),
  // },
  {
    name: 'home',
    path: '/',
    component: AppLayout,
    children: [
      {
        name: 'projects',
        path: 'projects',
        component: () => import('../pages/project/Projects.vue'),
      },
      {
        name: 'projects',
        path: 'projects/:id',
        props: true,
        component: () => import('../pages/project/Project.vue'),
      },
      // {
      //   name: 'biosamples',
      //   path: 'biosamples',
      //   component: () => import('../pages/admin/dashboard/BioSample.vue'),
      // },      
      // {
      //   name: 'analysis',
      //   path: 'analysis',
      //   component: () => import('../pages/admin/dashboard/Analysis.vue'),
      // },      
      // {
      //   name: 'experiments',
      //   path: 'experiments',
      //   component: () => import('../pages/admin/dashboard/Experiment.vue'),
      // },      {
      //   name: 'files',
      //   path: 'files',
      //   component: () => import('../pages/admin/dashboard/File.vue'),
      // },
      // {
      //   name: 'statistics',
      //   path: 'statistics',
      //   component: RouteViewComponent,
      //   children: [
      //     {
      //       name: 'charts',
      //       path: 'charts',
      //       component: () => import('../pages/admin/statistics/charts/Charts.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Charts',
      //       },
      //     },
      //     {
      //       name: 'progress-bars',
      //       path: 'progress-bars',
      //       component: () => import('../pages/admin/statistics/progress-bars/ProgressBars.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Progress-Bars',
      //       },
      //     },
      //   ],
      // },
      // {
      //   name: 'forms',
      //   path: 'forms',
      //   component: RouteViewComponent,
      //   children: [
      //     {
      //       name: 'analysis',
      //       path: 'analysis',
      //       component: () => import('../pages/admin/forms/Analysis.vue'),
      //     },
      //     {
      //       name: 'biosamples',
      //       path: 'biosamples',
      //       component: () => import('../pages/admin/forms/BioSample.vue'),
      //     },
      //     {
      //       name: 'experiments',
      //       path: 'experiments',
      //       component: () => import('../pages/admin/forms/Experiment.vue'),
      //     },
      //     {
      //       name: 'files',
      //       path: 'files',
      //       component: () => import('../pages/admin/forms/File.vue'),
      //     },
      //   ],
      // },
      // {
      //   name: 'maps',
      //   path: 'maps',
      //   component: RouteViewComponent,
      //   children: [
      //     {
      //       name: 'maplibre-maps',
      //       path: 'maplibre-maps',
      //       component: () => import('../pages/admin/maps/maplibre-maps/MapLibreMapsPage.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Maps',
      //       },
      //     },
      //     {
      //       name: 'yandex-maps',
      //       path: 'yandex-maps',
      //       component: () => import('../pages/admin/maps/yandex-maps/YandexMapsPage.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Maps',
      //       },
      //     },
      //     {
      //       name: 'leaflet-maps',
      //       path: 'leaflet-maps',
      //       component: () => import('../pages/admin/maps/leaflet-maps/LeafletMapsPage.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Maps',
      //       },
      //     },
      //     {
      //       name: 'bubble-maps',
      //       path: 'bubble-maps',
      //       component: () => import('../pages/admin/maps/bubble-maps/BubbleMapsPage.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Maps',
      //       },
      //     },
      //     {
      //       name: 'line-maps',
      //       path: 'line-maps',
      //       component: () => import('../pages/admin/maps/line-maps/LineMapsPage.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Maps',
      //       },
      //     },
      //   ],
      // },
      // {
      //   name: 'tables',
      //   path: 'tables',
      //   component: RouteViewComponent,
      //   children: [
      //     {
      //       name: 'markup',
      //       path: 'markup',
      //       component: () => import('../pages/admin/tables/markup-tables/MarkupTables.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Tables',
      //       },
      //     },
      //     {
      //       name: 'data',
      //       path: 'data',
      //       component: () => import('../pages/admin/tables/data-tables/DataTables.vue'),
      //       meta: {
      //         wikiLink: 'https://github.com/epicmaxco/vuestic-admin/wiki/Tables',
      //       },
      //     },
      //   ],
      // },
      // {
      //   name: 'pages',
      //   path: 'pages',
      //   component: RouteViewComponent,
      //   children: [
      //     {
      //       name: '404-pages',
      //       path: '404-pages',
      //       component: () => import('../pages/admin/pages/404PagesPage.vue'),
      //     },
      //     {
      //       name: 'faq',
      //       path: 'faq',
      //       component: () => import('../pages/admin/pages/FaqPage.vue'),
      //     },
      //   ],
      // },
      // UIRoute,
    ],
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

export default router
