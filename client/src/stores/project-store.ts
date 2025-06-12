import { defineStore } from 'pinia'
import { ProjectSchema, ResearchModel } from '../data/types'
import ProjectService from '../services/clients/ProjectService'
import { catchError } from '../composables/toastMessages'

const initForm: ProjectSchema = {
  project_id: '',
  name: '',
  version: '',
  description: '',
  models: []
}

const initModel: ResearchModel = {
  name: '',
  description: '',
  fields: [],
  id_format: [],
}

export const useProjectStore = defineStore('project', {
  state: () => {
    return {
      projectForm: { ...initForm } as ProjectSchema,
      showModelForm:false,
      projectIdExists: false,
      projectStats: [] as [string, number][],
      fromTemplate: false,
      showArchiveModal: false,
      selectedModel: undefined as ResearchModel | undefined,
      showUseTemplateModal: false,
      formStep: 0,
      isLoading: false,
      schema: null as ProjectSchema | null, //used for forms etc
      isArchived: false, //used for project status 
      projects: [] as ProjectSchema[],
      total: 0,
      models: [] as ResearchModel[],
      mappedModels: [] as { name: string, refModel: string | undefined, counts: number }[]
    }
  },
  actions: {
    resetProjectForm() {
      this.projectForm = {
        project_id: '',
        name: '',
        version: '',
        description: '',
        models: []
      }
      this.formStep = 0
    },
    async getProjectSchema(projectId: string) {
      if (this.schema && this.schema.project_id === projectId) return
      try {
        this.isLoading = true
        const { data } = await ProjectService.getProjectSchema(projectId)
        this.models = [...data.models]
        this.schema = { ...data }
      } catch (err) {
        catchError(err)
      } finally {
        this.isLoading = false
      }
    },
    async getProjectStats(projectId: string) {
      try {
        this.isLoading = true
        const { data } = await ProjectService.lookupProject(projectId)
        //map stats into mapped models
        this.projectStats = Object.entries(data)
        this.mappedModels = this.models.map(({ name, reference_model }) => {
          const counts = this.projectStats.find(([k, v]) => k === name)?.[1] ?? 0
          return { name, refModel: reference_model, counts }
        })
      } catch (error) {
        catchError(error)
      } finally {
        this.isLoading = false
      }
    },
    async getProjectStatus(projectId: string) {
      try {
        this.isLoading = true
        const { data } = await ProjectService.getProject(projectId)
        this.isArchived = data.archived
      } catch (error) {
        catchError(error)
      } finally {
        this.isLoading = false
      }
    },
    async getProjects(query: Record<string, any>, role:string, name:string) {
      try {
        
        this.isLoading = true
        const { data } = role !== 'admin' ? await ProjectService.getUserProjects(name, query) : await ProjectService.getProjects(query)

        this.projects = [...data.data]
        this.total = data.total
      } catch (error) {
        catchError(error)
      } finally {
        this.isLoading = false
      }
    },
    addModel() {
      this.projectForm.models.push({ ...initModel })
    },
    deleteModel(idx: number) {
      const model = this.projectForm.models[idx]
      const linkedModels = this.projectForm.models.filter(m => m.reference_model === model.name).map(m => m.name)
      if (linkedModels.length) {
        this.projectForm.models = this.projectForm.models.filter(m => !linkedModels.includes(m.name))
      }
      this.projectForm.models = [...this.projectForm.models.slice(0, idx), ...this.projectForm.models.slice(idx + 1)]
    },
  },
})
