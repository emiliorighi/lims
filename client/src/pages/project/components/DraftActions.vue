<template>
    <va-card-actions align="right">
        <va-button :loading="isLoading" :disabled="!projectStore.project.project_id" @click="saveDraft" icon="save"
            :color="'info'">Save Draft</va-button>
        <va-button icon="download">YAML</va-button>
    </va-card-actions>
</template>
<script setup lang="ts">
import { AxiosError } from 'axios';
import ProjectService from '../../../services/clients/ProjectService';
import { useProjectStore } from '../../../stores/project-store';
import { useGlobalStore } from '../../../stores/global-store';
import { ref } from 'vue';

const isLoading = ref(false)
const projectStore = useProjectStore()
const { toast } = useGlobalStore()
async function saveDraft() {
    isLoading.value = true
    await checkDraftProjectExists(projectStore.project.project_id)
    if (projectStore.existingDraftProject === null){
        await createDraftProject()
    } 
    isLoading.value = false
}

async function checkDraftProjectExists(projectId: string) {
    try {
        const { data } = await ProjectService.getDraftProject(projectId)
        projectStore.existingDraftProject = { ...data }
    } catch (error) {
        const axiosError = error as AxiosError
        if (axiosError.response && axiosError.response.status === 404) {
            projectStore.existingDraftProject = null
        }
    }
}

async function createDraftProject() {
    try {
        const { data } = await ProjectService.createDraftProject(projectStore.project)
        toast({ color: "success", message: data.message, title: 'Draft Project created' })

    } catch (error) {
        const axiosError = error as AxiosError
        toast({ color: 'danger', message: `${axiosError.message}`, title: 'Error while creating a new draft Project', duration: 1500 })

    }
}



</script>