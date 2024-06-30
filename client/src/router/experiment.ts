import { RouteRecordRaw } from 'vue-router';

export const experiments: Array<RouteRecordRaw> = [

    // EXPERIMENTS
    {
      name: 'experiments',
      path: 'experiments',
      props: true,
      component: () => import('../pages/experiment/Experiments.vue'),
    },
    {
      name: 'experiment',
      path: 'experiments/:experimentId',
      props: true,
      component: () => import('../pages/experiment/Experiment.vue')
    },
    {
      path: 'experiments/form',
      name: 'experiment-form',
      component: () => import('../pages/experiment-form/ExperimentForm.vue'),
      props: true
    },
    {
      path: 'experiments/form/:experimentId',
      name: 'experiment-form-update',
      component: () => import('../pages/experiment-form/ExperimentForm.vue'),
      props: true
    },
    {
      path: 'experiments/upload',
      name: 'experiment-upload',
      component: () => import('../pages/experiment-form/ExperimentUpload.vue'),
      props: true
    },
  
  ]