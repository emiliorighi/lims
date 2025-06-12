<template>
    <div>
        <div class="row justify-space-between align-end">
            <div class="flex">
                <VaBreadcrumbs active-color="primary" class="va-text-bold" separator=">">
                    <VaBreadcrumbsItem class="cursor-pointer" @click="projectStore.showModelForm = false" label="Project Form" />
                    <VaBreadcrumbsItem class="cursor-pointer" v-if="projectStore.showModelForm"
                        :label="projectStore.selectedModel?.name ? 'Editing model:' + projectStore.selectedModel.name : 'Create model'" />
                </VaBreadcrumbs>
            </div>
        </div>
        <ProjectForm v-if="!projectStore.showModelForm" />
        <ModelForm v-else @submit="handleModel" @close="projectStore.showModelForm = false" :mode="projectStore.selectedModel ? 'edit-override' : 'create'"
            :incoming-model="projectStore.selectedModel" :existing-models="filteredModels"
            :project-id="projectStore.projectForm.project_id" :from-project="true" />

    </div>
</template>
<script setup lang="ts">
import { useProjectStore } from '../stores/project-store'
import { computed } from 'vue';
import ProjectForm from '../components/forms/ProjectForm.vue';
import { ResearchModel } from '../data/types';
import ModelForm from '../components/forms/ModelForm.vue';

const projectStore = useProjectStore()


const models = computed(() => projectStore.projectForm.models)
const filteredModels = computed(() => models.value.filter(n => n.name !== projectStore.selectedModel?.name))


function handleModel(model: ResearchModel) {
    const idx = projectStore.projectForm.models.findIndex(({ name }) => name === model.name)
    if (idx !== -1) {
        projectStore.projectForm.models[idx] = { ...model }
    } else {
        projectStore.projectForm.models.push({ ...model })
    }
    projectStore.selectedModel = undefined
    projectStore.showModelForm = false
}

</script>
<style scoped>
.cursor-pointer {
    cursor: pointer;
}

</style>