<template>
    <div>
        <div class="row justify-space-between align-end">
            <div class="flex">
                <h1 class="va-h1">Project Form</h1>
                <p class="va-text-secondary">
                    Create a new Project
                </p>
            </div>
        </div>
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <VaInnerLoading :loading="isLoading">
                    <VaForm ref="schemaForm">
                        <VaStepper @finish="submitProject" linear v-model="currentStep" :steps="steps">
                            <template #step-content-0>
                                <VaCard>
                                    <VaCardContent>
                                        <div class="row">
                                            <div class="flex">
                                                <h2 class="va-h3">Project information</h2>
                                                <p class="va-text-secondary">
                                                    Type the name and version that define your project, if the project
                                                    already
                                                    exists you can import it
                                                </p>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="flex lg12 md12 sm12 xs12">
                                                <DebounceInput
                                                    placeholder="Type a name of at least 3 characters (required)"
                                                    :parent-model="projectStore.projectForm.name"
                                                    label="Project Name (required)"
                                                    :rules="[(v: string) => v.length >= 3 || 'name is mandatory, at least 3 characters']"
                                                    @change="handleName" />
                                            </div>
                                            <div class="flex lg12 md12 sm12 xs12">
                                                <DebounceInput placeholder="example: 1.0.0 or 1.2 (required)"
                                                    label="Project Version (required)"
                                                    :parent-model="projectStore.projectForm.version"
                                                    :rules="[(v: string) => v.length > 0 || 'version is mandatory', (v: string) => !isVersionDuplicated(v) || 'You must change the version of the template']"
                                                    @change="handleVersion" />
                                            </div>
                                            <div class="flex lg12 md12 sm12 xs12">
                                                <VaInput placeholder="Description of the project (optional)"
                                                    label="Project Description (optional)"
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
                                                        <VaButton @click="showModal = !showModal" preset="primary"
                                                            color="secondary">Use Template</VaButton>
                                                    </VaCardActions>
                                                </VaCard>
                                            </div>

                                        </div>
                                    </VaCardContent>
                                </VaCard>
                            </template>
                            <template #step-content-1>
                                <VaCard>
                                    <VaCardContent>
                                        <div class="row">
                                            <div class="flex">
                                                <h2 class="va-h3">Models</h2>
                                                <p class="va-text-secondary">
                                                    A model can be considered as a TSV file. Add as many models as TSV
                                                    files you
                                                    have, or use the same TSV
                                                    file to split your entries in more models. In case your TSV files
                                                    reference
                                                    each other, fill the
                                                    reference model field with the name of the target model.
                                                </p>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div v-for="model, idx in refModels" class="flex lg12 md12 sm12 xs12">
                                                <VaCard color="backgroundElement">
                                                    <VaCardContent>
                                                        <div class="row align-center">
                                                            <div class="flex">
                                                                <div class="row align-center">
                                                                    <div class="flex">
                                                                        <h3 class="va-h6">
                                                                            {{ model.name }}
                                                                        </h3>
                                                                        <p class="va-text-secondary">{{
                                                                            model.description }}</p>
                                                                    </div>
                                                                    <div v-if="model.reference_model" class="flex">
                                                                        <VaChip color="backgroundElement" size="small"
                                                                            icon="fa-link">{{
                                                                                model.reference_model }}</VaChip>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="flex">
                                                                <div class="row">
                                                                    <div class="flex">
                                                                        <VaButton @click="editModel(model)"
                                                                            preset="primary" icon="fa-edit">
                                                                        </VaButton>
                                                                    </div>
                                                                    <div class="flex">
                                                                        <VaButton @click="projectStore.deleteModel(idx)"
                                                                            color="danger" preset="primary"
                                                                            icon="fa-trash"></VaButton>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </VaCardContent>
                                                </VaCard>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="flex">
                                                <VaButton @click="addModel"
                                                    :color="refModelNames.length ? 'primary' : 'danger'">Add New
                                                    Model
                                                </VaButton>
                                            </div>
                                        </div>
                                    </VaCardContent>
                                </VaCard>
                            </template>
                            <template #step-content-2>
                                <ProjectDetails :project="project" />
                            </template>
                        </VaStepper>
                    </VaForm>
                </VaInnerLoading>
            </div>
        </div>
        <ModelFormModal 
            v-model="showModelForm" 
            @submit="handleModel" 
            :existing-models="filteredModels" 
            :incoming-model="selectedModel" 
            mode="create"
        />
        <VaModal v-model="showModal" hide-default-actions closeButton>
            <div class="layout va-gutter-5">
                <h1 class="va-h3">Incoming Project</h1>
                <p class="va-text-secondary">Review the incoming project before
                    overwriting
                    your current form</p>
                <ProjectDetails v-if="existingProject" :project="existingProject" />
                <div class="row">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaButton :loading="templateLoading" block @click="useProject">Use
                            Project as Template
                        </VaButton>
                    </div>
                </div>
            </div>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { defineVaStepperSteps, useForm, useToast } from 'vuestic-ui'
import { useProjectStore } from '../stores/project-store'
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';
import AuthService from '../services/clients/AuthService';
import { computed, ref } from 'vue';
import ProjectService from '../services/clients/ProjectService';
import { ReseachProject, ResearchModel } from '../data/types';
import DebounceInput from '../components/inputs/DebounceInput.vue';
import ProjectDetails from '../components/cards/ProjectDetailsCard.vue';
import ModelFormModal from '../components/modals/ModelFormModal.vue';
import { useModelStore } from '../stores/model-store';

const { init } = useToast()
const { validate } = useForm('schemaForm')
const projectStore = useProjectStore()
const modelStore = useModelStore()
const router = useRouter()

const steps = ref(defineVaStepperSteps([
    {
        label: 'Project Information',
        beforeLeave: (step) => {
            step.hasError = !validate() || projectStore.projectIdExists
        }
    },
    {
        label: 'Models',
        beforeLeave: (step) => { step.hasError = !refModelNames.value.length },
    },
    {
        label: 'Review',
    }
]))

const selectedModel = ref<ResearchModel | undefined>()

const isLoading = ref(false)
const currentStep = ref(0)
const existingProject = ref<ReseachProject | null>(null)
const templateLoading = ref(false)
const showModal = ref(false)
const showModelForm = ref(false)

const refModels = computed(() => projectStore.projectForm.models)
const refModelNames = computed(() => refModels.value.map(({ name }) => name))
const filteredModels = computed(() => refModels.value.filter(n => n.name !== selectedModel.value?.name))
const project = computed(() => projectStore.projectForm)

async function handleName(v: string) {
    await updateProjectAndValidate('name', v)
}

async function handleVersion(v: string) {
    await updateProjectAndValidate('version', v)
}

function handleModel(model: ResearchModel) {
    const idx = refModels.value.findIndex(({ name }) => name === model.name)
    const { models } = projectStore.projectForm
    if (idx !== -1) {
        models[idx] = { ...model }
    } else {
        models.push({ ...model })
    }
    projectStore.projectForm.models = [...models]
    selectedModel.value = undefined
}

function addModel() {
    selectedModel.value = undefined
    showModelForm.value = true
}

function editModel(model: ResearchModel) {
    selectedModel.value = { ...model }
    showModelForm.value = true
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

async function useProject() {
    if (!existingProject.value) return
    projectStore.projectForm = { ...existingProject.value }
    projectStore.fromTemplate = true
    showModal.value = !showModal.value
}

async function submitProject() {
    isLoading.value = !isLoading.value
    try {
        const { data } = await AuthService.createResearchProject(projectStore.projectForm)
        init({ color: 'success', message: data })
        projectStore.resetProjectForm()
        router.push({ name: 'projects' })
    } catch (error) {
        const axiosError = error as AxiosError
        if (axiosError.response && axiosError.response.data) {
            if (Array.isArray(axiosError.response.data)) {
                axiosError.response.data.forEach((d: string) => {
                    init({ color: 'danger', message: d })
                })
            } else {
                init({ color: 'danger', message: axiosError.response.data as string })
            }
        }
        else {
            init({ color: 'danger', message: 'Unexpected Error' })
            console.error(error)
        }
    } finally {
        isLoading.value = !isLoading.value
    }
}

</script>
