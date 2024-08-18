import { RouteLocationNormalized } from 'vue-router';
import { useGlobalStore } from '../stores/global-store'

export function isAdmin() {
  const { user } = useGlobalStore()
  if (user.role !== 'admin') {
    return { name: 'unauthorized' }
  }
}

export function hasProjectAccess(to: RouteLocationNormalized) {
  const { user } = useGlobalStore()
  const { role, projects } = user
  if (role !== 'admin') {
    const projectId = to.params.projectId as string
    if (!projects.includes(projectId)) {
      return { name: 'unauthorized' }
    }
  }
}

export async function isAuthenticated() {
  const gStore = useGlobalStore()
  await gStore.checkUserIsLoggedIn()
  if (!gStore.isAuthenticated) return { name: 'login' }
}
