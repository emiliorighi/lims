import { defineStore } from 'pinia'

const initSchema: Record<string, any> = {
  project_id: '',
  name: '',
  description: '',
  version: '',
  experiment: {},
  sample: {},
}

const initSearchForm = {
  filter: '',
  sort_order: ''
}

const initPagination = {
  offset: 0,
  limit: 10,
}

export const useSchemaStore = defineStore('schema', {
  state: () => {
    return {
      schema: { ...initSchema },
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
    resetSchema() {
      this.schema = { ...initSchema }
    }
  },
})
