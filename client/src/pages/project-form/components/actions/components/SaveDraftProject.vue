<template>
    <div>
        {{ isDraftUpdated }}
        <VaButton color="success" :loading="isLoading" :disabled="isDraftUpdated" @click="saveDraft" icon="save">Save
            Draft</VaButton>
        <VaModal size="large" v-model="show" hide-default-actions>
            <VaCardBlock v-if="projectStore.incomingProject" horizontal>
                <h2 class="va-h2">{{
            projectStore.incomingProject.project_id }} already exists!</h2>
                <p class="va-text-secondary">Choose if you want to save the current changes or revert to the database
                    object</p>
                <VaCardBlock class="flex-auto">
                    <VaButton color="info" @click="updateDraftProject" icon-right="chevron_right"> Save Current Changes
                    </VaButton>
                    <ProjectOverviewCard :metadata="projectStore.currentProject" />
                </VaCardBlock>
                <VaDivider vertical />
                <VaCardBlock class="flex-auto">
                    <VaButton color="warning" @click="revertProject" icon="chevron_left"> Revert to
                        Database Object </VaButton>
                    <ProjectOverviewCard :metadata="projectStore.incomingProject" />
                </VaCardBlock>
            </VaCardBlock>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useProjectStore } from '../../../../../stores/project-store'
import ProjectService from '../../../../../services/clients/ProjectService'
import { AxiosError } from 'axios'
import ProjectOverviewCard from '../../../../../components/project/ProjectOverviewCard.vue'
import { useToast } from 'vuestic-ui/web-components'

const projectStore = useProjectStore()
const { init } = useToast()


const isLoading = ref(false)
const show = ref(false)


const isDraftUpdated = computed(() => {
    return projectStore.incomingProject !== null && deepEqual(projectStore.currentProject, projectStore.incomingProject)
})

async function saveDraft() {

    await checkDraftProjectExists(projectStore.currentProject.project_id)

    if (projectStore.draftProjectExists) {
        show.value = !show.value
    } else {
        await createDraftProject()
    }
}

function revertProject() {

}

async function updateDraftProject() {
    try {
        isLoading.value = !isLoading.value
        const { project_id, ...projectData } = projectStore.currentProject
        const { data } = await ProjectService.updateDraftProject(project_id, projectData)
        init({ color: "success", message: data.message, title: 'Draft project updated', duration: 1500 })
        projectStore.incomingProject = { ...projectStore.currentProject }
        projectStore.draftProjectExists = true
    } catch (error) {
        const axiosError = error as AxiosError
        init({ color: "danger", message: axiosError.message, title: 'Something happened', duration: 1500 })
    } finally {
        isLoading.value = !isLoading.value

    }
}
async function checkDraftProjectExists(projectId: string) {
    try {
        isLoading.value = !isLoading.value
        const { data } = await ProjectService.getDraftProject(projectId)
        projectStore.incomingProject = { ...data }
        projectStore.draftProjectExists = true
    } catch (error) {
        const axiosError = error as AxiosError
        if (axiosError.response && axiosError.response.status === 404) {
            projectStore.draftProjectExists = false
        }
    } finally {
        isLoading.value = !isLoading.value
    }
}

async function createDraftProject() {
    try {
        isLoading.value = !isLoading.value
        init({ color: 'info', message: 'Saving Draft Project..' })
        const { data } = await ProjectService.createDraftProject(projectStore.currentProject)
        init({ color: "success", message: 'Draft Project saved!' })
        projectStore.incomingProject = { ...projectStore.currentProject }
        projectStore.draftProjectExists = true
    } catch (error) {
        const axiosError = error as AxiosError
        init({ color: 'danger', message: `${axiosError.message}`, title: 'Error while creating a new draft Project', duration: 1500 })
    } finally {
        isLoading.value = !isLoading.value
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