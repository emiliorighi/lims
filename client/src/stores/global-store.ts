import { defineStore } from 'pinia'
import { useToast, useColors } from 'vuestic-ui'
import { LinkType, ModelKeys, Theme } from '../data/types';
import AuthService from '../services/clients/AuthService';
import { catchError } from '../composables/toastMessages';
import StatsService from '../services/clients/StatsService';

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

const initCounts: Record<ModelKeys, number> = {
  models: 0,
  records: 0,
  projects: 0,
  protocols: 0,
  images: 0
}
export const useGlobalStore = defineStore('global', {
  state: () => {
    return {
      isSidebarVisible: true,
      user: { ...initUser },
      loading: false,
      counts: {
        ...initCounts
      } as Record<ModelKeys, number>,
      userForm: { ...initUserForm },
      isAuthenticated: isAuth,
      recordStats: [] as [string, number][],
      protocolStats: [] as [string, number][],
      imageStats: [] as [string, number][],
      showDeleteConfirmation: false,
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
      this.user = { ...initUser }
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
    async lookupData() {
      try {
        this.loading = true
        const { data } = await StatsService.lookupData()
        this.counts = { ...data }
      } catch (error) {
        catchError(error)
      } finally {
        this.loading = false
      }
    },
    async getRecordStats(field: string, query: Record<string, any>) {
      try {
        this.loading = true
        const { data } = await StatsService.getRecordStats(field, query)
        this.recordStats = Object.entries(data)
      } catch (error) {
        catchError(error)
      } finally {
        this.loading = false
      }
    },
    async getLinkStats(field: string, type: LinkType, query: Record<string, any>) {
      const q = { type, ...query }
      try {
        this.loading = true
        const { data } = await StatsService.getLinkStats(field, q)
        if (type === 'images') this.imageStats = Object.entries(data)
        else this.protocolStats = Object.entries(data)
      } catch (error) {
        catchError(error)
      } finally {
        this.loading = false
      }
    },
  },
})
