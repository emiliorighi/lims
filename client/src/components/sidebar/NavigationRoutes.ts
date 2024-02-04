export interface INavigationRoute {
  name: string
  displayName: string
  meta: { icon: string }
  children?: INavigationRoute[]
}

export default {
  root: {
    name: '/',
    displayName: 'projects',
  },
  routes: [
    {
      name: 'projects',
      displayName: 'projects',
      meta: {
        icon: 'vuestic-iconset-dashboard',
      },
    }
    // ,
    // {
    //   name: 'forms',
    //   displayName: 'forms',
    //   meta: {
    //     icon: 'vuestic-iconset-forms',
    //   },
    //   disabled: true,
    //   children: [
    //     {
    //       name: 'biosamples',
    //       displayName: 'biosamples',
    //     },
    //     {
    //       name: 'experiments',
    //       displayName: 'experiments',
    //     },
    //     {
    //       name: 'analysis',
    //       displayName: 'analysis',
    //     },
    //     {
    //       name: 'files',
    //       displayName: 'files',
    //     },
    //   ],
    // }
  ] as INavigationRoute[],
}
