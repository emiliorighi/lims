<template>

  <VaLayout :top="{ fixed: true, order: 3 }"
    :left="{ fixed: true, absolute: breakpoints.smDown, order: 2, overlay: breakpoints.smDown && isLeftSidebarVisible }"
    :right="{ fixed: true, absolute: breakpoints.smDown, order: 2, overlay: breakpoints.smDown && isRightSidebarVisible }"
    :bottom="{ fixed: true, order: 4 }" @left-overlay-click="isLeftSidebarVisible = false"
    @right-overlay-click="isRightSidebarVisible = false">
    <template #top>
      <VaNavbar shadowed>
        <template #left>
          <VaAvatar @click="isLeftSidebarVisible = !isLeftSidebarVisible" />
        </template>
      </VaNavbar>
    </template>

    <template #left>
      <VaSidebar v-model="isLeftSidebarVisible">
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
    </template>

    <!-- <template #right>
      <VaSidebar v-model="isRightSidebarVisible">

      </VaSidebar>
    </template> -->

    <template #content>
      <main>
        <div class="layout fluid va-gutter-5">
          <!-- <BreadCrumbs /> -->
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
import { ref, watchEffect, watch } from 'vue'
import { useBreakpoint } from 'vuestic-ui'
import BreadCrumbs from '../components/ui/BreadCrumbs.vue'
import { useRoute } from 'vue-router'

const breakpoints = useBreakpoint()
const route = useRoute()

const isLeftSidebarVisible = ref(breakpoints.smUp)
const isRightSidebarVisible = ref(breakpoints.smUp)

watchEffect(() => {
  isLeftSidebarVisible.value = breakpoints.smUp
  isRightSidebarVisible.value = breakpoints.smUp
})

watch(isLeftSidebarVisible, (newValue) => {
  if (breakpoints.smDown && newValue) {
    isRightSidebarVisible.value = false
  }
})

watch(isRightSidebarVisible, (newValue) => {
  if (breakpoints.smDown && newValue) {
    isLeftSidebarVisible.value = false
  }
})

function isRouteActive(name: string) {
  return name === route.name || route.fullPath.includes(name)
}
const menu = [
  { icon: "dashboard", title: "Dashboard", name: 'home' },
  { icon: "folder", title: "Projects", name: 'projects' },
  { icon: "edit", title: "Project Form", name: 'project-form' },
  // { "icon": "drafts", "title": "Draft Projects",name:'projects' },
  //     { "icon": "fa-vial", "title": "Samples" },
  //     { "icon": "fa-dna", "title": "Experiments" }
]

const subMenu = [
  { icon: 'settings', title: 'Settings' },
  { icon: 'github', title: 'Open Issue' },
  { icon: 'logout', title: 'Logout' },
]
</script>
