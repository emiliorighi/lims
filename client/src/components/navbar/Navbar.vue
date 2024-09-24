<template>
  <VaNavbar shadowed>
    <template #left>
      <div class="row align-center">
        <VaButton size="large" class="flex" preset="secondary"
          :icon="globalStore.isSidebarVisible ? 'menu_open' : 'menu'"
          @click="globalStore.isSidebarVisible = !globalStore.isSidebarVisible" />
        <span v-if="globalStore.user.name" class="flex">{{ globalStore.user.name }}</span>
      </div>
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

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useColors } from "vuestic-ui";
import { useGlobalStore } from "../../stores/global-store"
import { Theme } from "../../data/types"

const { currentPresetName } = useColors();
const globalStore = useGlobalStore()

onMounted(() => {
  globalStore.loadThemeLocalStorage()
})

const switchValue = computed({
  get() { return currentPresetName.value as Theme },
  set(value: Theme) {
    globalStore.setTheme(value)
  }
})

</script>
