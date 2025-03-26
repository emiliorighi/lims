<template>
    <VaLayout v-if="schema" :top="{ fixed: true, order: 2 }"
        :left="{ fixed: true, absolute: breakpoints.smDown, order: 1, overlay: breakpoints.smDown && isSidebarVisible }">
        <template #top>
            <VaNavbar>
                <template #left>
                    <VaNavbarItem>
                        <VaButton preset="secondary" :icon="isSidebarVisible ? 'menu_open' : 'menu'"
                            @click="isSidebarVisible = !isSidebarVisible" />
                    </VaNavbarItem>
                    <VaNavbarItem>
                        <span class="va-h6">
                            {{ schema.name }} {{ schema.version }}
                        </span>
                    </VaNavbarItem>
                </template>
                <template #right>
                    <VaButton icon="fa-plus" :to="{ name: 'modelForm' }" preset="primary" color="textPrimary">
                        Model
                    </VaButton>
                    <VaButton :to="{ name: 'uploadData' }" color="textPrimary" preset="secondary" icon="fa-file-upload">
                        Data
                    </VaButton>
                </template>
            </VaNavbar>
            <VaDivider style="margin: 0" />
        </template>
        <template #left>
            <VaSidebar activeColor="textPrimary" v-model="isSidebarVisible">
                <VaSidebarItem :active="route.name === 'projectSchema'"
                    :to="{ name: 'projectSchema', params: { projectId } }">
                    <VaSidebarItemContent>
                        <VaIcon name="dashboard" />
                        <VaSidebarItemTitle>
                            Project Dashboard
                        </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                </VaSidebarItem>
                <VaAccordion>
                    <VaCollapse>
                        <template #header="{ value: isCollapsed }">
                            <VaSidebarItem :active="route.name === 'projectModel'">
                                <VaSidebarItemContent>
                                    <VaIcon name="fa-note-sticky" />
                                    <VaSidebarItemTitle>Models</VaSidebarItemTitle>
                                    <VaSpacer />
                                    <VaIcon :name="isCollapsed ? 'va-arrow-up' : 'va-arrow-down'" />
                                </VaSidebarItemContent>
                            </VaSidebarItem>
                        </template>
                        <template #body>
                            <VaSidebarItem :active="isRouteActive(name)" v-for="{ name } in models" :key="name"
                                :to="{ name: 'projectModel', params: { modelName: name } }">
                                <VaSidebarItemContent>
                                    <VaSidebarItemTitle class="va-text-capitalize">
                                        {{ name }}
                                    </VaSidebarItemTitle>
                                </VaSidebarItemContent>
                            </VaSidebarItem>
                        </template>
                    </VaCollapse>
                </VaAccordion>
                <VaSpacer />
                <VaSidebarItem :to="{ name: 'projects' }">
                    <VaSidebarItemContent>
                        <VaIcon name="fa-arrow-left"></VaIcon>
                        <VaSidebarItemTitle>
                            Back to Projects
                        </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                </VaSidebarItem>
            </VaSidebar>
        </template>
        <template #content>
            <main>
                <div class="layout va-gutter-5">
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <router-view v-slot="{ Component }">

                                <Transition name="fade">
                                    <component :is="Component" />
                                </Transition>


                            </router-view>
                        </div>
                    </div>
                </div>
            </main>
        </template>
    </VaLayout>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useBreakpoint, VaSidebar } from 'vuestic-ui'
import { useSchemaStore } from '../stores/schema-store';
import { useRoute } from 'vue-router';

const breakpoints = useBreakpoint()
const isSidebarVisible = ref(breakpoints.smUp)

const props = defineProps<{
    projectId: string
}>()

const route = useRoute()

const schemaStore = useSchemaStore()

const schema = computed(() => schemaStore.schema)
const models = computed(() => schema.value?.models ?? [])

watch(() => props.projectId, async () => {
    await schemaStore.getProjectSchema(props.projectId)
}, { immediate: true })

function isRouteActive(name: string) {
    return route.params.modelName === name
}


</script>
