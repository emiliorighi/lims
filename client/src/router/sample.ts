import { RouteRecordRaw } from 'vue-router';

export const samples: Array<RouteRecordRaw> = [
  
    // SAMPLES
    {
      path: '/projects/:projectId/samples',
      name: 'samples',
      component: () => import('../pages/sample/Samples.vue'),
      props: true
    },
    {
      name: 'sample',
      path: '/projects/:projectId/samples/:sampleId',
      props: true,
      component: () => import('../pages/sample/Sample.vue')
    },
    {
      path: '/projects/:projectId/samples/form',
      name: 'sample-form',
      component: () => import('../pages/sample-form/SampleForm.vue'),
      props: true
    },
    {
      path: '/projects/:projectId/samples/form/:sampleId',
      name: 'sample-form-update',
      component: () => import('../pages/sample-form/SampleForm.vue'),
      props: true
    },
    {
      path: '/projects/:projectId/samples/upload',
      name: 'sample-upload',
      component: () => import('../pages/sample-form/SamplesUpload.vue'),
      props: true
    }
  
  ]