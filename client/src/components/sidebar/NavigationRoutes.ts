export interface INavigationRoute {
  name: string
  displayName: string
  meta: { icon: string }
  children?: INavigationRoute[]
}

export default {
  root: {
    name: '/',
    displayName: 'navigationRoutes.home',
  },
  routes: [
    {
      name: 'dashboard',
      displayName: 'dashboard',
      meta: {
        icon: 'vuestic-iconset-dashboard',
      },
    },
    {
      name: 'forms',
      displayName: 'forms',
      meta: {
        icon: 'vuestic-iconset-forms',
      },
      disabled: true,
      children: [
        {
          name: 'biosamples',
          displayName: 'biosamples',
        },
        {
          name: 'experiments',
          displayName: 'experiments',
        },
        {
          name: 'analysis',
          displayName: 'analysis',
        },
        {
          name: 'files',
          displayName: 'files',
        },
      ],
    },
    // {
    // //   name: 'tables',
    // //   displayName: 'tables',
    // //   meta: {
    // //     icon: 'vuestic-iconset-tables',
    // //   },
    // //   children: [
    // //     {
    // //       name: 'markup',
    // //       displayName: 'markupTables',
    // //     },
    // //     // {
    // //     //   name: 'data',
    // //     //   displayName: 'dataTables',
    // //     // },
    // //   ],
    // // },
    // {
    //   name: 'ui',
    //   displayName: 'uiElements',
    //   meta: {
    //     icon: 'vuestic-iconset-ui-elements',
    //   },
    //   disabled: true,
    //   children: [
    //     {
    //       name: 'buttons',
    //       displayName: 'buttons',
    //     },
    //     {
    //       name: 'cards',
    //       displayName: 'cards',
    //     },
    //     {
    //       name: 'chat',
    //       displayName: 'chat',
    //     },
    //     {
    //       name: 'chips',
    //       displayName: 'chips',
    //     },
    //     {
    //       name: 'collapses',
    //       displayName: 'collapses',
    //     },
    //     {
    //       name: 'colors',
    //       displayName: 'colors',
    //     },
    //     // {
    //     //   name: 'color-pickers',
    //     //   displayName: 'colorPickers',
    //     // },
    //     {
    //       name: 'file-upload',
    //       displayName: 'fileUpload',
    //     },
    //     {
    //       name: 'grid',
    //       displayName: 'grid',
    //     },
    //     {
    //       name: 'icon-sets',
    //       displayName: 'icons',
    //       children: [
    //         {
    //           displayName: 'concrete',
    //           name: 'icon-set',
    //         },
    //       ],
    //     },
    //     {
    //       name: 'lists',
    //       displayName: 'lists',
    //     },
    //     {
    //       name: 'modals',
    //       displayName: 'modals',
    //     },
    //     {
    //       name: 'notifications',
    //       displayName: 'notifications',
    //     },
    //     {
    //       name: 'popovers',
    //       displayName: 'popovers',
    //     },
    //     {
    //       name: 'rating',
    //       displayName: 'rating',
    //     },
    //     {
    //       name: 'sliders',
    //       displayName: 'sliders',
    //     },
    //     {
    //       name: 'spacing',
    //       displayName: 'spacing',
    //     },
    //     {
    //       name: 'spinners',
    //       displayName: 'spinners',
    //     },
    //     {
    //       name: 'tabs',
    //       displayName: 'tabs',
    //     },
    //     // {
    //     //   name: "timelines",
    //     //   displayName: "timelines",
    //     // },
    //     {
    //       name: 'tree-view',
    //       displayName: 'treeView',
    //     },
    //     {
    //       name: 'typography',
    //       displayName: 'typography',
    //     },
    //   ],
    // },
    // {
    //   name: 'maps',
    //   displayName: 'maps',
    //   meta: {
    //     icon: 'vuestic-iconset-maps',
    //   },
    //   disabled: true,
    //   children: [
    //     {
    //       name: 'maplibre-maps',
    //       displayName: 'maplibre-maps',
    //     },
    //     {
    //       name: 'yandex-maps',
    //       displayName: 'yandex-maps',
    //     },
    //     {
    //       name: 'leaflet-maps',
    //       displayName: 'leaflet-maps',
    //     },
    //     {
    //       name: 'bubble-maps',
    //       displayName: 'bubble-maps',
    //     },
    //     {
    //       name: 'line-maps',
    //       displayName: 'line-maps',
    //     },
    //   ],
    // },
    // {
    //   name: 'pages',
    //   displayName: 'pages',
    //   meta: {
    //     icon: 'vuestic-iconset-files',
    //   },
    //   disabled: true,
    //   children: [
    //     {
    //       name: 'login',
    //       displayName: 'login-singup',
    //     },
    //     {
    //       name: '404-pages',
    //       displayName: '404-pages',
    //     },
    //     {
    //       name: 'faq',
    //       displayName: 'faq',
    //     },
    //   ],
    // },
  ] as INavigationRoute[],
}
