<template>
  <div class="app-layout">
    <navbar />
    <div class="app-layout__content">
      <div class="app-layout__sidebar-wrapper" :class="{ minimized: isSidebarMinimized }">
        <div v-if="isFullScreenSidebar" class="d-flex justify-end">
          <va-button class="px-4 py-4" icon="md_close" preset="plain" color="dark" @click="onCloseSidebarButtonClick" />
        </div>
        <sidebar :width="sidebarWidth" :minimized="isSidebarMinimized" :minimized-width="sidebarMinimizedWidth"
          :animated="!isMobile" />
      </div>
      <div class="app-layout__page">
        <div id="scroll-container" class="layout fluid va-gutter-5">
          <VaBreadcrumbs color="primary">
            <VaBreadcrumbsItem :to="bc.path" v-for="bc in breadcrumbs" :label="bc.name" />
          </VaBreadcrumbs>
          <VaDivider />
          <router-view v-slot="{ Component }">
            <Transition name="fade">
              <component :is="Component" />
            </Transition>
          </router-view>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router'
import { useGlobalStore } from '../stores/global-store'
import Navbar from '../components/navbar/Navbar.vue'
import Sidebar from '../components/sidebar/Sidebar.vue'

const route = useRoute()
const router = useRouter()
const GlobalStore = useGlobalStore()

const mobileBreakPointPX = 640
const tabletBreakPointPX = 768

const sidebarWidth = ref('16rem')
const sidebarMinimizedWidth = ref(undefined)

const isMobile = ref(false)
const isTablet = ref(false)
const { isSidebarMinimized } = storeToRefs(GlobalStore)
const checkIsTablet = () => window.innerWidth <= tabletBreakPointPX
const checkIsMobile = () => window.innerWidth <= mobileBreakPointPX

const onResize = () => {
  isSidebarMinimized.value = checkIsTablet()

  isMobile.value = checkIsMobile()
  isTablet.value = checkIsTablet()
  sidebarMinimizedWidth.value = isMobile.value ? '0' : '4.5rem'
  sidebarWidth.value = isTablet.value ? '100%' : '16rem'
}

const breadcrumbs = computed(() => {
  const pathArray = route.path.split('/').filter(Boolean);
  const breadcrumbArray = [];
  let accumulatedPath = '';

  for (let i = 0; i < pathArray.length; i++) {
    accumulatedPath += '/' + pathArray[i];

    // Check if we are at a dynamic segment and replace it with actual value
    const matchedRoute = router.getRoutes().find(r => {
      const pathSegments = r.path.split('/').filter(Boolean);
      if (pathSegments.length === pathArray.length) {
        let isMatch = true;
        for (let j = 0; j <= i; j++) {
          if (pathSegments[j].startsWith(':')) continue; // Ignore dynamic segments
          if (pathSegments[j] !== pathArray[j]) {
            isMatch = false;
            break;
          }
        }
        return isMatch;
      }
      return false;
    });

    if (matchedRoute) {
      const name = pathArray[i]
      breadcrumbArray.push({
        name,
        path: accumulatedPath,
      });
    }
  }

  return breadcrumbArray;
});


onMounted(() => {
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
})

onBeforeRouteUpdate(() => {
  if (checkIsTablet()) {
    // Collapse sidebar after route change for Mobile
    isSidebarMinimized.value = true
  }
})

onResize()

const isFullScreenSidebar = computed(() => isTablet.value && !isSidebarMinimized.value)

const onCloseSidebarButtonClick = () => {
  isSidebarMinimized.value = true
}
</script>

<style lang="scss">
$mobileBreakPointPX: 640px;
$tabletBreakPointPX: 768px;

.p-0 {
  padding: 0;
}

.app-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;

  &__navbar {
    min-height: 4rem;
  }

  &__content {
    display: flex;
    height: calc(100vh - 4rem);
    flex: 1;

    @media screen and (max-width: $tabletBreakPointPX) {
      height: calc(100vh - 6.5rem);
    }

    .app-layout__sidebar-wrapper {
      position: relative;
      height: 100%;
      background: #ffffff;

      @media screen and (max-width: $tabletBreakPointPX) {
        &:not(.minimized) {
          width: 100%;
          height: 100%;
          position: fixed;
          top: 0;
          z-index: 999;
        }

        .va-sidebar:not(.va-sidebar--minimized) {
          .va-sidebar__menu {
            padding: 0;
          }
        }
      }
    }
  }

  &__page {
    flex-grow: 2;
    overflow-y: scroll;
  }
}

.row-equal .flex {
  .va-card {
    height: 100%;
  }
}
</style>
