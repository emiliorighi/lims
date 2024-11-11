import { defineStore } from 'pinia'
import { useToast, useColors } from 'vuestic-ui'
import { Theme } from '../data/types';
import AuthService from '../services/clients/AuthService';

const STORAGE_KEY = 'theme';
const savedTheme = localStorage.getItem(STORAGE_KEY) || 'light'
const { init } = useToast()

const AUTH_KEY = 'auth'
const isAuth = localStorage.getItem(AUTH_KEY) === 'true'
const initUser = {
  name: '',
  role: '',
  projects: [] as string[]
}
const initUserForm = {
  name: '',
  password: ''
}
export const useGlobalStore = defineStore('global', {
  state: () => {
    return {
      isSidebarVisible: true,
      user: { ...initUser },
      userForm: { ...initUserForm },
      isAuthenticated: isAuth,
      showDeleteConfirmation:false,
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

    changeUserName(name: string) {
      this.user.name = name
    },
    mapUser(data: Record<string, any>) {
    
      this.user.name = data.name
      this.user.role = data.role
      localStorage.setItem(AUTH_KEY, 'true');
      this.isAuthenticated = true
    },

    async login(name: string, password: string) {
      try {
        const { data } = await AuthService.login({ name, password })
        this.mapUser(data)
        this.toast({ message: `Welcome ${this.user.name}!`, color: 'success' })
      } catch (error) {
        console.log(error)
        this.toast({ message: 'Bad user or password', color: 'danger' })
        this.isAuthenticated = false
        localStorage.setItem(AUTH_KEY, 'false');
      }
    },
    async logout() {
      await AuthService.logout()
      this.user = {...initUser}
      localStorage.setItem(AUTH_KEY, 'false');
      this.isAuthenticated = false
    },
    async checkUserIsLoggedIn() {
      if (!this.isAuthenticated) return
      try {
        const { data } = await AuthService.check()
        this.mapUser(data)
      } catch (error) {
        console.error(error)
        localStorage.setItem(AUTH_KEY, 'false');
      }
    },
  },
})
