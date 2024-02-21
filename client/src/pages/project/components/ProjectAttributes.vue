<template>
    <div class="row">
        <div class="flex lg8 md8">
            <h2 class="va-h4">Project information</h2>
            <p>Define a name and a version of the project. The project identifier will be generated combining the name and
                the
                version</p>
        </div>
    </div>
    <VaDivider></VaDivider>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <va-input placeholder="Type a name of at least 3 characters (required)"
                :rules="[(v: string) => v.length >= 3 || 'name is mandatory, at least 3 characters']" class="mt-4"
                label="name (required)" v-model="projectStore.project.name" />
            <va-input placeholder="example: 1.0.0 or 1.2 (required)" class="mt-4" label="version (required)"
                v-model="projectStore.project.version" :rules="[(v: string) => v.length > 0 || 'version is mandatory']" />
            <va-input class="mt-4" label="Project Identifier" placeholder="Type a name and a version"
                :loading="isIdValidationLoading" readonly v-model="projectStore.project.project_id"
                :rules="[!idAlreadyExists || 'Project Id already present']"></va-input>
            <va-input class="mt-4" placeholder="Description of the project (optional)"
                label="Project description (optional)" v-model="projectStore.project.description" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watchEffect } from 'vue';
import { useProjectStore } from '../../../stores/project-store';
import ProjectService from '../../../services/clients/ProjectService';
import { AxiosError } from 'axios';

const projectStore = useProjectStore()
const idAlreadyExists = ref(false)
const isIdValidationLoading = ref(false)
const mergedId = computed(() => {
    if (projectStore.project.name && projectStore.project.version) return `${projectStore.project.name}_${projectStore.project.version}`
    return ''
})

watchEffect(async () => {
    if (mergedId.value.length === 0) return
    try {
        isIdValidationLoading.value = true
        const { data } = await ProjectService.getProject(mergedId.value)
        idAlreadyExists.value = true
    } catch (error) {
        const axiosError = error as AxiosError
        if (axiosError.response && axiosError.response.status === 404) {
            idAlreadyExists.value = false
        }
    } finally {
        projectStore.project.project_id = mergedId.value
        isIdValidationLoading.value = false
    }
})
</script>