import { defineStore } from 'pinia'
import { useToast, useColors } from 'vuestic-ui'
import { Theme } from '../data/types';
import AuthService from '../services/clients/AuthService';

const STORAGE_KEY = 'theme';
const savedTheme = localStorage.getItem(STORAGE_KEY) || 'light'
const { init } = useToast()

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
      isSidebarVisible: false,
      user: { ...initUser },
      userForm: { ...initUserForm },
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

    changeUserName(name: string) {
      this.user.name = name
    },
    async loginUser() {
      try {
        const { name, password } = this.userForm
        const { data } = await AuthService.login({ name, password })
        if (data) {
          this.user = { ...data.user }
          this.isAuthenticated = true
          init({ message: data.message, color: 'success' })
          this.userForm = {...initUserForm}
        }
      } catch (err) {
        console.error(err)
        init({ message: 'Bad user or password', color: 'danger' })
      }
    },

    async logoutUser() {
      try {
        await AuthService.logout()
        this.user = { ...initUser }
        this.isAuthenticated = false
      } catch (error) {
        console.error('An unexpected error occurred during authentication check.');
      }
    },

    async checkUserIsLoggedIn() {
      try {
        const { data } = await AuthService.check()
        this.user = { ...data }
        this.isAuthenticated = true
      } catch (error) {
        console.error(error)
        console.error('An unexpected error occurred during authentication check.');
        this.isAuthenticated = false
      }
    }
  },
})
