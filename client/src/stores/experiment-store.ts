import { defineStore } from 'pinia'
import { ExperimentModel, ModelSearchForm } from '../data/types'

const defaultExperiment: ExperimentModel = {
  experiment_id: '',
  sample_id: '',
  metadata: {}
}

const initSearchForm: ModelSearchForm = {
  filter: '',
  query: {},
  sort_column: '',
  sort_order: 'asc'
}

const initPagination = {
  offset: 0,
  limit: 10,
}

export const useExperimentStore = defineStore('experiment', {
  state: () => {
    return {
      experiment: { ...defaultExperiment },
      showForm: false,
      showReport: false,
      expIdToUpdate: undefined as string | undefined,
      searchForm: { ...initSearchForm },
      pagination: { ...initPagination },
    }
  },

  actions: {
    resetSeachForm() {
      this.searchForm = { ...initSearchForm }
    },
    resetPagination() {
      this.pagination = { ...initPagination }
    },
    resetExperiment() {
      this.experiment = { ...defaultExperiment }
    }
  },
})
