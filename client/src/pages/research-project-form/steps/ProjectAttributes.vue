<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <DebounceInput placeholder="Type a name of at least 3 characters (required)"
                :parent-model="projectStore.projectForm.name" label="Project Name (required)"
                :rules="[(v: string) => v.length >= 3 || 'name is mandatory, at least 3 characters']"
                @change="handleName" />
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <DebounceInput placeholder="example: 1.0.0 or 1.2 (required)" label="Project Version (required)"
                :parent-model="projectStore.projectForm.version"
                :rules="[(v: string) => v.length > 0 || 'version is mandatory', (v: string) => !isVersionDuplicated(v) || 'You must change the version of the template']"
                @change="handleVersion" />
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput placeholder="Description of the project (optional)" label="Project Description (optional)"
                v-model="projectStore.projectForm.description" />
        </div>
    </div>
    <div v-if="projectStore.projectIdExists" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard stripe stripe-color="danger">
                <VaCardContent>
                    <h6 class="va-h6">
                        Project '{{ mergedId }}' already exists!
                    </h6>
                    <p>You can use this project as a template but you <span
                            class="va-text-bold va-text-danger">MUST</span> change the version
                    </p>
                </VaCardContent>
                <VaCardActions>
                    <VaButton @click="showModal = !showModal" preset="primary" color="secondary">Use Template</VaButton>
                </VaCardActions>
            </VaCard>
        </div>
        <VaModal v-model="showModal" hide-default-actions closeButton>
            <div class="layout va-gutter-5">
                <h1 class="va-h3">Incoming Project</h1>
                <p class="va-text-secondary">Review the incoming project before overwriting your current form</p>
                <ProjectDetails v-if="existingProject" :project="existingProject" />
                <div class="row">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaButton :loading="templateLoading" block @click="useProject">Use Project as Template
                        </VaButton>
                    </div>
                </div>
            </div>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useProjectStore } from '../../../stores/project-store';
import { useToast } from 'vuestic-ui/web-components';
import ProjectService from '../../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import { ReseachProject } from '../../../data/types';
import DebounceInput from '../../../components/inputs/DebounceInput.vue';
import ProjectDetails from '../../../components/project/ProjectDetails.vue';

const projectStore = useProjectStore()

const existingProject = ref<ReseachProject | null>(null)
const { init } = useToast()
const isLoading = ref(false)
const templateLoading = ref(false)
const projectFromTemplate = ref(false)
const showModal = ref(false)

async function handleName(v: string) {
    await updateProjectAndValidate('name', v)
}

async function handleVersion(v: string) {
    await updateProjectAndValidate('version', v)
}

async function updateProjectAndValidate(
    field: 'name' | 'version',
    value: string
) {
    projectStore.projectForm[field] = trimmedValue(value)
    const { name, version } = projectStore.projectForm

    // Validate field-specific conditions.
    if (field === 'name' && name.length < 3) return
    if (field === 'version' && !version) return

    // When both fields are truthy, validate the project.
    if (name && version) {
        await validateProject()
    }
}

const trimmedValue = (v: string) => v.trim().replace(' ', '')


const mergedId = computed(() => `${projectStore.projectForm.name}_${projectStore.projectForm.version}`)

function isVersionDuplicated(v: string) {
    return projectFromTemplate.value && existingProject.value?.version === v
}

async function validateProject() {
    try {
        isLoading.value = true
        const { data } = await ProjectService.getProjectSchema(mergedId.value)
        existingProject.value = data
        projectStore.projectIdExists = true
    } catch (error) {
        const axiosError = error as AxiosError;
        if (axiosError.response && axiosError.response.status === 404) {
            isLoading.value = false
            // set project id
            projectStore.projectForm.project_id = mergedId.value
            projectStore.projectIdExists = false
        } else {
            console.error('Error fetching:', error);
            init({ message: 'Error fetching: ' + error, color: 'danger' })
        }
        existingProject.value = null
    } finally {
        isLoading.value = false
    }
}

async function useProject() {
    if (!existingProject.value) return
    const { name, version, description,project_id } = existingProject.value
    const project = { name, version, description, project_id }
    try {
        templateLoading.value = true
        const { data } = await ProjectService.getProjectModels(project_id)
        projectStore.projectForm = { models: data.data, ...project }
        projectFromTemplate.value = true
        showModal.value = !showModal.value
    }catch(error){

    }finally{
        templateLoading.value = false

    }

}

</script>