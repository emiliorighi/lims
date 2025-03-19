import { defineStore } from 'pinia'
import { ProjectSchema } from '../data/types'
import ProjectService from '../services/clients/ProjectService'
import { useToast } from 'vuestic-ui/web-components'

const initSchema: ProjectSchema = {
  project_id: '',
  name: '',
  description: '',
  version: '',
  models: []
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
      schema: null as ProjectSchema | null,
      showReport: false,
      isLoading: false,
      showForm: false,
      showDetails: false,
      showSchema: false,
      showChart: false,
      searchForm: { ...initSearchForm },
      pagination: { ...initPagination },
      toast: useToast().init
    }
  },

  actions: {
    async getProjectSchema(projectId: string) {
      try {
        this.isLoading = true
        const { data } = await ProjectService.getProjectSchema(projectId)
        this.schema = { ...data }
      } catch (err) {
        this.toast({ message: err as string, color: 'danger' })
      } finally {
        this.isLoading = false
      }
    },
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
