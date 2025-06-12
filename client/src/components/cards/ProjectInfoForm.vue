<template>
    <VaCard>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h2 class="va-h3">Project information</h2>
                    <p class="va-text-secondary">
                        Type the name and version of your project, if the project
                        already
                        exists you can use it as a template
                    </p>
                </div>
            </div>
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
                                    class="va-text-bold va-text-danger">MUST</span> change
                                the
                                version
                            </p>
                            <p><span class="va-text-bold">NOTE: </span> Protocols and images
                                of the related models should be imported separatedly</p>
                        </VaCardContent>
                        <VaCardActions>
                            <VaButton @click="projectStore.showUseTemplateModal = !projectStore.showUseTemplateModal" preset="primary" color="secondary">Use Template
                            </VaButton>
                        </VaCardActions>
                    </VaCard>
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { useToast } from 'vuestic-ui'
import { useProjectStore } from '../../stores/project-store'
import { AxiosError } from 'axios';
import { computed, ref } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import { ReseachProject } from '../../data/types';
import DebounceInput from '../../components/inputs/DebounceInput.vue';

const { init } = useToast()
const projectStore = useProjectStore()


const isLoading = ref(false)
const existingProject = ref<ReseachProject | null>(null)

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
    return projectStore.fromTemplate && existingProject.value?.version === v
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

</script>
