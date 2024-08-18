<template>
  <VaNavbar shadowed>
    <template #left>
      <div class="row align-center">
        <VaButton class="flex" preset="secondary" :icon="globalStore.isSidebarVisible ? 'menu_open' : 'menu'"
          @click="globalStore.isSidebarVisible = !globalStore.isSidebarVisible" />
        <span v-if="globalStore.user.name" class="flex">{{ globalStore.user.name }}</span>
      </div>
    </template>
    <template #center>
      <Transition name="fade">
        <h4 v-if=isProjectView style="margin: 0;" class="va-h4">
          <TypingAnimation :text="`${schemaStore.schema.name} ${schemaStore.schema.version}`" />
        </h4>
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

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useColors } from "vuestic-ui";
import { useSchemaStore } from "../../stores/schemas-store"
import { useGlobalStore } from "../../stores/global-store"
import { Theme } from "../../data/types"
import TypingAnimation from "../ui/TypingAnimation.vue"

const { currentPresetName } = useColors();
const schemaStore = useSchemaStore()
const globalStore = useGlobalStore()
const route = useRoute()

onMounted(() => {
  globalStore.loadThemeLocalStorage()
})

const isProjectView = computed(() => {
  return !!route.params.projectId
})

const switchValue = computed({
  get() { return currentPresetName.value as Theme },
  set(value: Theme) {
    globalStore.setTheme(value)
  }
})

</script>
