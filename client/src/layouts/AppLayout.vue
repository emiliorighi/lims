<template>
  <VaLayout :top="{ fixed: true, order: 3 }" :left="{ fixed: true, absolute: breakpoints.smDown, order: 2, }"
    @left-overlay-click="globalStore.isSidebarVisible = !globalStore.isSidebarVisible">
    <template #top>
      <VaNavbar shadowed>
        <template #left>
          <VaNavbarItem>
            <VaButton size="large" class="flex" preset="secondary"
              :icon="globalStore.isSidebarVisible ? 'menu_open' : 'menu'"
              @click="globalStore.isSidebarVisible = !globalStore.isSidebarVisible" />
          </VaNavbarItem>
        </template>
        <template #right>
          <VaNavbarItem>
            <VaButton href="https://github.com/emiliorighi/lims/issues/new" target="_blank" icon="github"
              color="textPrimary" preset="secondary"></VaButton>
          </VaNavbarItem>
          <VaNavbarItem>
            <VaButton :to="{ name: 'docs' }" icon="fa-circle-question" color="textPrimary" preset="secondary">
            </VaButton>
          </VaNavbarItem>
          <VaNavbarItem>
            <VaButtonDropdown preset="primary" left-icon icon="fa-user" stick-to-edges :label="globalStore.user.name">
              <div class="layout va-gutter-3 fluid">
                <div class="row align-center">
                  <div class="flex">
                    <p>Theme:</p>
                  </div>
                  <div class="flex">
                    <VaSwitch size="small" v-model="switchValue" color="#5123a1" off-color="#ffd300" true-value="dark"
                      false-value="light" style="--va-switch-checker-background-color: #252723;">
                      <template #innerLabel>
                        <div class="va-text-center">
                          <VaIcon :name="switchValue === 'light' ? 'light_mode' : 'dark_mode'" />
                        </div>
                      </template>
                    </VaSwitch>
                  </div>
                </div>
                <div class="row">
                  <div class="flex lg12 md12 sm12 xs12">
                    <VaButton v-if="globalStore.isAuthenticated" block @click="logout" color="textPrimary"
                      preset="secondary" icon="logout">
                      Logout
                    </VaButton>
                    <VaButton v-else block :to="{ name: 'login' }" color="textPrimary" preset="secondary" icon="login">
                      Login
                    </VaButton>
                  </div>
                </div>
              </div>
            </VaButtonDropdown>
          </VaNavbarItem>
        </template>
      </VaNavbar>
    </template>
    <template #left>
      <div style="display: flex; height: 100%;">
        <VaSidebar v-model="globalStore.isSidebarVisible">
          <VaSidebarItem :active="isRouteActive('home')" :to="{ name: 'home' }">
            <VaSidebarItemContent>
              <VaIcon name="fa-house" />
              <VaSidebarItemTitle>
                Home
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </VaSidebarItem>
          <VaSidebarItem :active="isRouteActive('projects')" :to="{ name: 'projects' }">
            <VaSidebarItemContent>
              <VaIcon name="fa-diagram-project" />
              <VaSidebarItemTitle>
                Projects
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </VaSidebarItem>
          <VaSidebarItem v-if="isAdmin" :active="isRouteActive(name)" v-for="{ icon, title, name } in adminMenu"
            :key="icon" :to="{ name: name }">
            <VaSidebarItemContent>
              <VaIcon :name="icon" />
              <VaSidebarItemTitle>
                {{ title }}
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </VaSidebarItem>
        </VaSidebar>
      </div>
    </template>
    <template #content>
      <main>
        <div class="layout va-gutter-5 fluid">
          <router-view v-slot="{ Component }">
            <Transition name="fade">
              <component :is="Component" />
            </Transition>
          </router-view>
        </div>
      </main>
    </template>
  </VaLayout>
</template>
<script setup lang="ts">
import { useBreakpoint, useColors } from 'vuestic-ui'
import { useGlobalStore } from "../stores/global-store"
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Theme } from '../data/types'

const globalStore = useGlobalStore()
const breakpoints = useBreakpoint()
const { currentPresetName } = useColors();
const route = useRoute()
const router = useRouter()

const adminMenu = [
  { icon: "fa-plus", title: "Project Form", name: 'project-form' },
  { icon: "fa-users", title: "Users", name: 'users' },
]

onMounted(async () => {
  globalStore.loadThemeLocalStorage()
  await globalStore.checkUserIsLoggedIn()
})

const isAdmin = computed(() => {
  return globalStore.user.role === 'admin'
})

const switchValue = computed({
  get() { return currentPresetName.value as Theme },
  set(value: Theme) {
    globalStore.setTheme(value)
  }
})

function isSubRouteActive(name: string) {
  return name === route.name
}

function isRouteActive(name: string) {
  return isSubRouteActive(name) || route.fullPath.includes(name)
}

async function logout() {
  await globalStore.logout()
  router.push({ name: 'home' })
}


</script>
