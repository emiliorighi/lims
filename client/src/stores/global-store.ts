import { defineStore } from 'pinia'
import { useToast } from 'vuestic-ui'
const { init } = useToast()

export const useGlobalStore = defineStore('global', {
  state: () => {
    return {
      isSidebarMinimized: true,
      userName: 'User',
      toast: init
    }
  },

  actions: {
    toggleSidebar() {
      this.isSidebarMinimized = !this.isSidebarMinimized
    },

    changeUserName(userName: string) {
      this.userName = userName
    },
  },
})
