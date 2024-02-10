<template>
    <VaModal size="large" @cancel="projectStore.existingDraftProject = null" close-button
        :model-value="!!projectStore.existingDraftProject" hide-default-actions overlay-opacity="0.2">
        <template #header>
            <h3 class="va-h3" v-if="projectStore.existingDraftProject !== null">{{
                projectStore.existingDraftProject.project_id }} already exists!</h3>
        </template>

        <VaCardBlock v-if="projectStore.existingDraftProject" horizontal>
            <VaCardBlock class="flex-auto">
                <VaButton color="info" @click="updateDraftProject" icon-right="chevron_right"> Overwrite Existing Draft
                </VaButton>
                <ProjectOverviewCard :metadata="projectStore.project" />
            </VaCardBlock>
            <VaDivider vertical />
            <VaCardBlock class="flex-auto">
                <VaButton color="warning" @click="projectStore.overwriteProject" icon="chevron_left"> Overwrite
                    Current Draft </VaButton>
                <ProjectOverviewCard :metadata="projectStore.existingDraftProject" />
            </VaCardBlock>
        </VaCardBlock>
    </VaModal>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../../stores/project-store'
import { useGlobalStore } from '../../../stores/global-store'
import ProjectService from '../../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import ProjectOverviewCard from './ProjectOverviewCard.vue';

const projectStore = useProjectStore()
const { toast } = useGlobalStore()

async function updateDraftProject() {
    try {
        const { project_id, ...projectData } = projectStore.project
        const { data } = await ProjectService.updateDraftProject(project_id, projectData)
        toast({ color: "success", message: data.message, title: 'Draft project updated', duration: 1500 })
        projectStore.resetDraftProject()
    } catch (error) {
        const axiosError = error as AxiosError
        toast({ color: "danger", message: axiosError.message, title: 'Something happened', duration: 1500 })
    }
}



</script>