<template>
    <div class="row">
        <div class="flex">
            <h1 class="va-h1">Create a new project</h1>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInnerLoading :loading="isLoading">
                <VaForm ref="schemaForm">
                    <VaStepper class="stepper-custom" @finish="submitProject" linear v-model="projectStore.formStep"
                        :steps="steps">
                        <template #step-content-0>
                            <ProjectInfoForm />
                        </template>
                        <template #step-content-1>
                            <ModelsForm />
                        </template>
                        <template #step-content-2>
                            <ProjectDetails :project="project" />
                        </template>
                    </VaStepper>
                </VaForm>
            </VaInnerLoading>
        </div>
    </div>

    <VaModal v-model="projectStore.showUseTemplateModal" hide-default-actions closeButton>
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
</template>
<script setup lang="ts">
import { defineVaStepperSteps, useForm, useToast } from 'vuestic-ui'
import { useProjectStore } from '../../stores/project-store'
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';
import AuthService from '../../services/clients/AuthService';
import { computed, onMounted, ref } from 'vue';
import { ReseachProject } from '../../data/types';
import ProjectDetails from '../../components/cards/ProjectDetailsCard.vue';
import ProjectInfoForm from '../../components/cards/ProjectInfoForm.vue';
import ModelsForm from '../cards/ModelsForm.vue';

const { init } = useToast()
const { validate } = useForm('schemaForm')
const projectStore = useProjectStore()
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
        beforeLeave: (step) => { step.hasError = !modelNames.value.length },
    },
    {
        label: 'Review',
    }
]))


const isLoading = ref(false)
const existingProject = ref<ReseachProject | null>(null)
const templateLoading = ref(false)
const models = computed(() => projectStore.projectForm.models)
const modelNames = computed(() => models.value.map(({ name }) => name))
const project = computed(() => projectStore.projectForm)


async function useProject() {
    if (!existingProject.value) return
    projectStore.projectForm = { ...existingProject.value }
    projectStore.fromTemplate = true
    projectStore.showUseTemplateModal = !projectStore.showUseTemplateModal
}

onMounted(() => {
    validate() // validate the form to avoid errors when the form is mounted
})

async function submitProject() {
    if (!validate()) {
        init({ color: 'danger', message: 'Please fill all the required fields' })
        return
    }
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
<style>


.va-stepper__step-content-wrapper--vertical {
    min-height: 500px;
    width: 100% !important;
}
</style>