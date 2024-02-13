import { defineStore } from 'pinia'
import { SampleModel } from '../data/types'

const defaultSample: SampleModel = {
  sample_id: '',
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

export const useSampleStore = defineStore('sample', {
  state: () => {
    return {
      sample: null as SampleModel | null,
      isUpdate: false,
      searchForm: { ...initSearchForm },
      pagination: { ...initPagination },
    }
  },

  actions: {
    resetSeachForm() {
      this.searchForm = { ...initSearchForm }
    },
    initSample(){
      this.sample = {...defaultSample}
    },
    resetPagination() {
      this.pagination = { ...initPagination }
    },
    resetSample() {
      this.sample = null
    }
  },
})
