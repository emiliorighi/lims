<template>
    <VaLayout :top="{ fixed: true, order: 2 }"
        :left="{ fixed: true, absolute: breakpoints.smDown, order: 1, overlay: breakpoints.smDown && isSidebarVisible }">
        <template #top>
            <VaNavbar shadowed bordered color="backgroundPrimary">
                <template #left>
                    <VaNavbarItem>
                        <VaButton preset="secondary" :icon="isSidebarVisible ? 'menu_open' : 'menu'"
                            @click="isSidebarVisible = !isSidebarVisible" />   
                    </VaNavbarItem>
                    <VaNavbarItem>
                        <div class="row align-end">
                            <div class="flex">
                                <span class="va-h4">
                                    {{ projectStore.schema?.name }}
                                </span>
                            </div>
                            <div class="flex">
                                <span class="va-text-secondary">
                                    {{ projectStore.schema?.version }}
                                </span>
                                <span v-if="isArchived" class="va-text-secondary">
                                    (archived)
                                </span>
                            </div>
                        </div>
                    </VaNavbarItem>
                </template>
            </VaNavbar>
        </template>
        <template #left>
            <VaSidebar v-model="isSidebarVisible">
                <VaSidebarItem :active="route.name === 'project'" :to="{ name: 'project', params: { projectId } }">
                    <VaSidebarItemContent>
                        <VaIcon name="fa-book-open" />
                        <VaSidebarItemTitle>
                            Project Details
                        </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                </VaSidebarItem>
                <VaAccordion>
                    <VaCollapse>
                        <template #header="{ value: isCollapsed }">
                            <VaSidebarItem>
                                <VaSidebarItemContent>
                                    <VaIcon name="fa-cube" />
                                    <VaSidebarItemTitle>Models</VaSidebarItemTitle>
                                    <VaSpacer />
                                    <VaIcon :name="isCollapsed ? 'va-arrow-up' : 'va-arrow-down'" />
                                </VaSidebarItemContent>
                            </VaSidebarItem>
                        </template>
                        <template #body>
                            <VaSidebarItem :to="{ name: 'details', params: { modelName: name, projectId } }"
                                :active="isRouteActive(name)" v-for="{ name, reference_model } in models" :key="name">
                                <VaSidebarItemContent>
                                    <VaSidebarItemTitle class="va-text-capitalize">
                                        {{ name }}
                                    </VaSidebarItemTitle>
                                    <VaChip color="backgroundElement" size="small" icon="fa-link"
                                        v-if="reference_model">{{
                                            reference_model }}</VaChip>
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
                <div class="layout va-gutter-5 fluid">
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <router-view v-if="projectStore.schema" v-slot="{ Component }">
                                <Transition name="fade">
                                    <component :is="Component" />
                                </Transition>
                            </router-view>
                        </div>
                    </div>
                </div>
            </main>
            <ArchiveProjectModal :archive="archiveAction.value" :project-id="projectId" />
            <ModelFormModal v-model="modelStore.showCreateModal" mode="create" :existing-models="models"
                :is-project-form="false" @submit="submitModel" />
        </template>
    </VaLayout>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useBreakpoint, useToast, VaSidebar } from 'vuestic-ui'
import {  useRoute, useRouter } from 'vue-router';
import { useProjectStore } from '../stores/project-store';
import ModelFormModal from '../components/modals/ModelFormModal.vue';
import { useModelStore } from '../stores/model-store';
import { ResearchModel } from '../data/types';
import AuthService from '../services/clients/AuthService';
import { catchError } from '../composables/toastMessages';
import ArchiveProjectModal from '../components/modals/ArchiveProjectModal.vue';

const props = defineProps<{
    projectId: string
}>()

const route = useRoute()
const router = useRouter()
const { init } = useToast()
const breakpoints = useBreakpoint()
const projectStore = useProjectStore()
const modelStore = useModelStore()

const isLoading = ref(false)
const isSidebarVisible = ref(breakpoints.smUp)

const models = computed(() => projectStore.models)
const isArchived = computed(() => projectStore.isArchived)
const archiveAction = computed(() => isArchived.value ?
    {
        icon: 'fa-unlock',
        label: 'Reactivate',
        value: false,
    } :
    {
        icon: 'fa-lock',
        label: 'Archive',
        value: true,
    })



watch(() => props.projectId, async () => {
    await projectStore.getProjectSchema(props.projectId)
    await projectStore.getProjectStatus(props.projectId)
    isSidebarVisible.value = true
}, { immediate: true })

function isRouteActive(name: string) {
    return route.params.modelName === name
}

async function submitModel(model: ResearchModel) {
    let success = false
    try {
        isLoading.value = true
        await AuthService.createModel(props.projectId, { ...model })
        init({ color: 'success', message: `${model.name} created` })
        success = true
    } catch (error) {
        success = false
        catchError(error)
    } finally {
        isLoading.value = false
        if (success) {
            //fecth updated project
            await projectStore.getProjectSchema(props.projectId)
            router.push({ name: 'project', params: { projectId: props.projectId } })
        }
    }

}

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
