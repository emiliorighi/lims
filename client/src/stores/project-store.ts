import { defineStore } from 'pinia'
import { SchemaForm } from '../data/types'
import { useToast } from 'vuestic-ui/web-components'

const { init } = useToast()

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
      currentProject: { ...initProject }, // the one holding the values from the form
      incomingProject: null as SchemaForm | null, //the draft one from the database with same project_id
      projectExists: false,
      draftProjectExists: false,
      confirmOverwrite: false
    }
  },

  actions: {
    overwriteProject() {
      if (this.incomingProject) {
        
        if(this.incomingProject.valid){
          const {valid, ...projectData} = this.incomingProject
          this.currentProject = { ...projectData }
        }else{
          this.currentProject = { ...this.incomingProject }
        }
        init({ message: `Project ${this.currentProject.project_id} uploaded`, color: 'success' })
      }
    },
    switchConfirm(){
      this.confirmOverwrite = !this.confirmOverwrite
    },
    // overWriteDraftProject() {
    //   if (this.incomingProject) {
    //     this.incomingProject = { ...this.project }
    //   }
    // },
    resetProject() {
      this.currentProject = { ...initProject }
    },
    resetDraftProject() {
      this.incomingProject = null
    }
  },
})
