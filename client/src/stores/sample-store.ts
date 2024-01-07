import { defineStore } from 'pinia'

const initSample: Record<string, any> = {
  id: '',
  user: '',
  project: '',
  version: '',
  metadata: {}
}

const initSearchForm = {
  filter: '',
  sort_order: ''
}

const initPagination = {
  offset: 0,
  limit: 10,
}

export const useSampleStore = defineStore('schema', {
  state: () => {
    return {
      sample: { ...initSample },
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
    resetSample() {
      this.sample = { ...initSample }
    }
  },
})
