import { defineStore } from 'pinia'
import { ProjectSchema, ReseachProject, SchemaForm } from '../data/types'
import { useToast } from 'vuestic-ui/web-components'

const { init } = useToast()

const initForm: ProjectSchema = {
  project_id: '',
  name: '',
  version: '',
  description: '',
  models: []
}

export const useProjectStore = defineStore('project', {
  state: () => {
    return {
      projectForm: {...initForm} as ProjectSchema,
      projectIdExists: false
    }
  },

  actions: {
    resetProjectForm() {
      this.projectForm = { ...initForm }
    },
  },
})
