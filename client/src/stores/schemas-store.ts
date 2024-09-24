import { defineStore } from 'pinia'
import { ModelType, SchemaForm } from '../data/types'

const initSchema: SchemaForm = {
  project_id: '',
  name: '',
  description: '',
  version: '',
  experiment: {
    id_format: [],
    fields: []
  },
  sample: {
    id_format: [],
    fields: []
  },
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
      showReport: false,
      showForm: false,
      showDetails: false,
      showSchema: false,
      showChart: false,
      model: 'sample' as ModelType,
      searchForm: { ...initSearchForm },
      pagination: { ...initPagination },
    }
  },

  actions: {
    resetSearchForm() {
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
