<template>
    <div>
        <VaModal size="large" @cancel="projectStore.incomingProject = null" close-button
            :model-value="!!projectStore.incomingProject" hide-default-actions overlay-opacity="0.2">
            <template #header>
                <h3 class="va-h3" v-if="projectStore.incomingProject !== null">{{
                projectStore.incomingProject.project_id }} already exists!</h3>
            </template>
            <VaCardBlock
                v-if="projectStore.incomingProject && deepEqual(projectStore.currentProject, projectStore.incomingProject)">
                The draft project is up to date!
            </VaCardBlock>
            <VaCardBlock v-else-if="projectStore.incomingProject" horizontal>
                <VaCardBlock class="flex-auto">
                    <VaButton color="info" @click="updateDraftProject" icon-right="chevron_right"> Overwrite Existing
                        Draft
                    </VaButton>
                    <ProjectOverviewCard :metadata="projectStore.currentProject" />
                </VaCardBlock>
                <VaDivider vertical />
                <VaCardBlock class="flex-auto">
                    <VaButton color="warning" @click="projectStore.overwriteProject" icon="chevron_left"> Overwrite
                        Current Draft </VaButton>
                    <ProjectOverviewCard :metadata="projectStore.incomingProject" />
                </VaCardBlock>
            </VaCardBlock>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../../stores/project-store'
import { useGlobalStore } from '../../../stores/global-store'
import ProjectService from '../../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import ProjectOverviewCard from '../../../components/project/ProjectOverviewCard.vue';

const projectStore = useProjectStore()
const { toast } = useGlobalStore()

async function updateDraftProject() {
    try {
        const { project_id, ...projectData } = projectStore.currentProject
        const { data } = await ProjectService.updateDraftProject(project_id, projectData)
        toast({ color: "success", message: data.message, title: 'Draft project updated', duration: 1500 })
        projectStore.resetDraftProject()
    } catch (error) {
        const axiosError = error as AxiosError
        toast({ color: "danger", message: axiosError.message, title: 'Something happened', duration: 1500 })
    }
}

function deepEqual(currentProject: Record<string, any>, incomingProject: Record<string, any>) {
    // Check if both arguments are objects
    if (typeof currentProject !== 'object' || typeof incomingProject !== 'object' || currentProject === null || incomingProject === null) {
        return currentProject === incomingProject; // Check for strict equality if not objects
    }

    // Get the keys of both objects
    var keys1 = Object.keys(currentProject);
    var keys2 = Object.keys(incomingProject);

    // Check if the number of keys is the same
    if (keys1.length !== keys2.length) {
        return false;
    }

    // Check if all keys in currentProject exist in incomingProject and have the same value (recursively)
    for (var key of keys1) {
        if (!keys2.includes(key) || !deepEqual(currentProject[key], incomingProject[key])) {
            return false;
        }
    }

    // If all checks pass, the objects are considered equal
    return true;
}


</script>