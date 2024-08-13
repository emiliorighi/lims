<template>
  <VaNavbar class="nav-h">
    <template #left>
      <VaButton size="large" preset="secondary" :icon="isSidebarVisible ? 'menu_open' : 'menu'"
        @click="isSidebarVisible = !isSidebarVisible" />
      <VaBreadcrumbs class="va-title" color="primary">
        <VaBreadcrumbsItem :to="bc.path" v-for="bc in breadcrumbs" :label="bc.name" />
      </VaBreadcrumbs>
    </template>
    <template #right>
      <div class="row justify-end align-center" style="gap: 1rem;">
        <div class="flex">
          <VaButton size="large" preset="secondary" color="secondary" target="_blank"
            href="https://github.com/emiliorighi/lims/issues/new" icon="github">
          </VaButton>
        </div>
        <div class="flex">
          <VaSwitch v-model="switchValue" color="#5123a1" off-color="#ffd300" true-value="dark" false-value="light"
            style="--va-switch-checker-background-color: #252723;">
            <template #innerLabel>
              <div class="va-text-center">
                <VaIcon :name="switchValue === 'light' ? 'light_mode' : 'dark_mode'" />
              </div>
            </template>
          </VaSwitch>
        </div>
      </div>
    </template>
  </VaNavbar>

</template>

<script setup lang="ts">
import { computed, ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBreakpoint } from 'vuestic-ui'
import { useColors } from "vuestic-ui";

const { applyPreset, currentPresetName } = useColors();

const switchValue = computed({
  get() { return currentPresetName.value },
  set(value) { applyPreset(value) }
})
export interface INavigationRoute {
  name: string
  displayName: string
  meta: { icon: string }
  children?: INavigationRoute[]
}
const breakpoints = useBreakpoint()

const route = useRoute()
const router = useRouter()
const isSidebarVisible = ref(breakpoints.mdUp)

watchEffect(() => {
  isSidebarVisible.value = breakpoints.smUp
})

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

</script>
