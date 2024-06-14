import { defineStore } from 'pinia'
import { ModelSearchForm, SampleModel } from '../data/types'

const defaultSample: SampleModel = {
  sample_id: '',
  metadata: {}
}

const initSearchForm: ModelSearchForm = {
  filters: {},
  sort_column: '',
  sort_order: 'asc'
}

const initPagination = {
  offset: 0,
  limit: 10,
}

export const useSampleStore = defineStore('sample', {
  state: () => {
    return {
      sample: null as SampleModel | null,
      showForm:false,
      isUpdate: false,
      searchForm: { ...initSearchForm },
      pagination: { ...initPagination },
    }
  },

  actions: {
    resetSeachForm() {
      this.searchForm = { ...initSearchForm }
    },
    initSample() {
      this.sample = { ...defaultSample }
    },
    resetPagination() {
      this.pagination = { ...initPagination }
    },
    resetSample() {
      this.sample = null
    }
  },
})
