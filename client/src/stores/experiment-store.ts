import { defineStore } from 'pinia'
import { ExperimentModel } from '../data/types'

const defaultSample: ExperimentModel = {
  experiment_id: '',
  sample_id:'',
  metadata: {}
}

const initSearchForm = {
  filters: {} as Record<string,any>,
  sort_column: '',
  sort_order: 'asc' as 'asc' | 'desc'
}

const initPagination = {
  offset: 0,
  limit: 10,
}

export const useExperimentStore = defineStore('experiment', {
  state: () => {
    return {
      experiment: null as ExperimentModel | null,
      isUpdate: false,
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

  },
})
