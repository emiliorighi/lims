<template>

  <VaLayout :top="{ fixed: true, order: 3 }" :left="{ fixed: true, absolute: breakpoints.smDown, order: 2, }"
    @left-overlay-click="isLeftSidebarVisible = false; isProjectBarVisible = false">
    <template #top>
      <VaNavbar shadowed>
        <template #left>
          <VaAvatar @click="isLeftSidebarVisible = !isLeftSidebarVisible; isProjectBarVisible = !isProjectBarVisible" />
        </template>
        <template #center>
          <Transition name="fade">
            <h4 v-if=isProjectView class="va-h4">{{ schemaStore.schema.project_id }}</h4>
          </Transition>
        </template>
        <template #right>
          <VaSwitch v-model="switchValue" color="#5123a1" off-color="#ffd300" true-value="dark" false-value="light"
            style="--va-switch-checker-background-color: #252723;">
            <template #innerLabel>
              <div class="va-text-center">
                <VaIcon :name="switchValue === 'light' ? 'light_mode' : 'dark_mode'" />
              </div>
            </template>
          </VaSwitch>
        </template>
      </VaNavbar>
    </template>
    <template #left>
      <div style="display: flex; height: 100%;">
        <VaSidebar :minimized="isProjectBarVisible" v-model="isLeftSidebarVisible">
          <VaSidebarItem :active="isRouteActive(name)" v-for="{ icon, title, name } in menu" :key="icon"
            :to="{ name: name }">
            <VaSidebarItemContent>
              <VaIcon :name="icon" />
              <VaSidebarItemTitle>
                {{ title }}
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </VaSidebarItem>
          <VaSidebarItem v-for="{ icon, title } in subMenu" :key="icon">
            <VaSidebarItemContent>
              <VaIcon :name="icon" />
              <VaSidebarItemTitle>
                {{ title }}
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </VaSidebarItem>
        </VaSidebar>
        <VaDivider vertical style="margin: 0;" />
        <VaSidebar hoverable minimized-width="64px" v-if="isProjectView" v-model="isProjectBarVisible">
          <VaSidebarItem :active="isSubRouteActive(m.name)" v-for="m in projectMenu" :key="m.name" :to="m.to">
            <VaSidebarItemContent>
              <VaIcon :name="m.icon" />
              <VaSidebarItemTitle>
                {{ m.label }}
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </VaSidebarItem>
        </VaSidebar>
      </div>
    </template>
    <template #content>
      <main>
        <div class="layout fluid va-gutter-5">
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
import { ref, watchEffect, watch, computed, onMounted } from 'vue'
import { useBreakpoint } from 'vuestic-ui'
import { useRoute } from 'vue-router'
import { useColors } from "vuestic-ui";
import { useSchemaStore } from "../stores/schemas-store"
import { useGlobalStore } from "../stores/global-store"
import { Theme } from "../data/types"

const { applyPreset, currentPresetName } = useColors();

const schemaStore = useSchemaStore()
const globalStore = useGlobalStore()

onMounted(() => {
  globalStore.loadThemeLocalStorage()
})

const projectMenu = computed(() => {
  const projectId = schemaStore.schema.project_id
  if (!projectId) return
  const tabs = [
    {
      label: 'Summary',
      icon: 'summarize',
      to: { name: 'project', params: { projectId: projectId } },
      name: 'project'
    },
    {
      label: 'Samples',
      icon: 'fa-vial',
      to: { name: 'samples' },
      name: 'samples'
    },
    {
      label: 'Experiments',
      icon: 'fa-dna',
      to: { name: 'experiments' },
      name: 'experiments'
    },
    {
      label: 'Upload',
      icon: 'upload',
      to: { name: 'upload' },
      name: 'upload'
    },
    {
      label: 'Statistics',
      icon: 'query_stats',
      to: { name: 'statistics' },
      name: 'statistics'
    }
  ]
  if (schemaStore.schema.experiment.id_format.length) {
    return tabs
  } return tabs.filter(t => t.name !== 'experiments')
})


const isProjectView = computed(() => {
  return route.meta.layout === 'project'
})

const switchValue = computed({
  get() { return currentPresetName.value as Theme },
  set(value: Theme) {
    globalStore.setTheme(value)
  }
})

const breakpoints = useBreakpoint()
const route = useRoute()

watch(isProjectView, () => {
  isProjectBarVisible.value = isProjectView.value
})

const isProjectBarVisible = ref(false)
const isLeftSidebarVisible = ref(breakpoints.smUp)

watchEffect(() => {
  isLeftSidebarVisible.value = breakpoints.smUp
})

function isSubRouteActive(name: string) {
  return name === route.name
}

function isRouteActive(name: string) {
  return isSubRouteActive(name) || route.fullPath.includes(name)
}

const menu = [
  { icon: "dashboard", title: "Dashboard", name: 'home' },
  { icon: "folder", title: "Projects", name: 'projects' },
  { icon: "edit", title: "Project Form", name: 'project-form' },
]

const subMenu = [
  { icon: 'settings', title: 'Settings' },
  { icon: 'github', title: 'Open Issue' },
  { icon: 'logout', title: 'Logout' },
]
</script>
