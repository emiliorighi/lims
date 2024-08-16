import { defineStore } from 'pinia'
import { useToast, useColors } from 'vuestic-ui'
import { Theme } from '../data/types';

const STORAGE_KEY = 'theme';
const savedTheme = localStorage.getItem(STORAGE_KEY) || 'light'
const { init } = useToast()

export const useGlobalStore = defineStore('global', {
  state: () => {
    return {
      isSidebarMinimized: true,
      userName: '',
      userRole: '',
      userPassword: '',
      userProjects: [] as string[],
      isAuthenticated: false,
      theme: savedTheme,
      toast: init
    }
  },

  actions: {
    setTheme(value: Theme) {
      this.theme = value;
      const { applyPreset } = useColors()
      applyPreset(this.theme)
      localStorage.setItem(STORAGE_KEY, this.theme);
    },

    loadThemeLocalStorage() {
      const savedState = localStorage.getItem(STORAGE_KEY);
      if (savedState) {
        this.theme = savedState
        const { applyPreset } = useColors()
        applyPreset(this.theme)

      }
    },

    changeUserName(userName: string) {
      this.userName = userName
    },
  },
})
