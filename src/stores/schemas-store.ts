import { defineStore } from 'pinia';

import * as analysis from '../../public/analysis-schema.json'
import * as biosample from '../../public/biosample-schema.json'
import * as experiment from '../../public/experiment-schema.json'

export const dbStore = defineStore('db', {
  state: () => {
    return {
      schemas: [analysis, biosample, experiment],
      biosamples:[],
      experiments:[],
      analysis:[],
      files:[]
    }
  },

  actions: {

    // toggleSidebar() {
    //   this.isSidebarMinimized = !this.isSidebarMinimized
    // },

    // changeUserName(userName: string) {
    //   this.userName = userName
    // },
  },
})
