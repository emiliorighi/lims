import { defineStore } from 'pinia'
import { SchemaForm } from '../data/types'

const initProject: SchemaForm = {
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


export const useProjectStore = defineStore('project', {
  state: () => {
    return {
      responseMessage: '',
      project: { ...initProject }, // the one holding the values from the form
      existingDraftProject: null as SchemaForm | null //the draft one from the database with same project_id
    }
  },

  actions: {
    overwriteProject() {
      if (this.existingDraftProject) {
        this.project = { ...this.existingDraftProject }
        this.resetDraftProject()
      }
    },
    // overWriteDraftProject() {
    //   if (this.existingDraftProject) {
    //     this.existingDraftProject = { ...this.project }
    //   }
    // },
    resetSchema() {
      this.project = { ...initProject }
    },
    resetProject() {
      this.project = { ...initProject }
    },
    resetDraftProject() {
      this.existingDraftProject = null
    }
  },
})
