<template>
    <h4 class="va-h4">Project Information</h4>
    <p class="va-text-secondary">Insert the basic information of the project</p>
    <ProjectConflictNotificationCard
        :text="`A project with id: ${mergedId} already exists! Use it as a template but change the version`"
        v-if="projectStore.projectExists" :existing-project="existingProject" />

    <ProjectConflictNotificationCard :text="` A draft project with id: ${mergedId} already exists!`"
        v-if="projectStore.draftProjectExists" :existing-project="existingDraftProject" />

    <div class="row">
        <VaInput class="flex lg4 md4 sm12 xs12" placeholder="Type a name of at least 3 characters (required)"
            :rules="[(v: string) => v.length >= 3 || 'name is mandatory, at least 3 characters', !projectStore.projectExists || 'Project Id already exists!']"
            label="name (required)" v-model="projectStore.currentProject.name" />

        <VaInput class="flex lg4 md4 sm12 xs12" placeholder="example: 1.0.0 or 1.2 (required)"
            label="version (required)" v-model="projectStore.currentProject.version"
            :rules="[(v: string) => v.length > 0 || 'version is mandatory', !projectStore.projectExists || 'Project Id already exists!']" />

        <VaInput class="flex lg4 md4 sm12 xs12" label="Project Identifier" placeholder="Type a name and a version"
            :loading="isIdValidationLoading" readonly v-model="mergedId"
            :rules="[!projectStore.projectExists || 'Project Id already exists!']"></VaInput>

        <VaInput class="flex lg6 md6 sm12 xs12" placeholder="Description of the project (optional)"
            label="Project description (optional)" v-model="projectStore.currentProject.description" />
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useProjectStore } from '../../../stores/project-store';
import ProjectService from '../../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import { SchemaForm } from '../../../data/types';
import ProjectConflictNotificationCard from '../../../components/cards/ProjectConflictNotificationCard.vue'

const projectStore = useProjectStore()
const existingProject = ref<SchemaForm | null>(null)
const existingDraftProject = ref<SchemaForm | null>(null)

const isIdValidationLoading = ref(false)
const mergedId = computed(() => {
    if (projectStore.currentProject.name && projectStore.currentProject.version) return `${projectStore.currentProject.name}_${projectStore.currentProject.version}`
    return ''
})



watch(() => mergedId.value, async () => {

    if (!mergedId.value || mergedId.value.length <= 3) return;

    isIdValidationLoading.value = true;

    await fetchProjectData(ProjectService.getProject, mergedId.value, existingProject);

    projectStore.projectExists = existingProject.value !== null

    if (!projectStore.projectExists) {

        await fetchProjectData(ProjectService.getDraftProject, mergedId.value, existingDraftProject);

        projectStore.draftProjectExists = existingDraftProject.value !== null
    }
    projectStore.currentProject.project_id = mergedId.value

    isIdValidationLoading.value = false;

});

// Abstracted function to fetch project data
async function fetchProjectData(fetchFn: (id: string) => Promise<any>, id: string, targetRef: any): Promise<void> {
    try {
        const { data } = await fetchFn(id);
        targetRef.value = { ...data };
    } catch (error) {
        const axiosError = error as AxiosError;
        if (axiosError.response && axiosError.response.status === 404) {
            targetRef.value = null;
        } else {
            console.error('Error fetching project data:', error);
        }
    }
}

</script>