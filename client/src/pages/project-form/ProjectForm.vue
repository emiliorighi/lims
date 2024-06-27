<template>
    <div>
        <Header :title="title" :description="description"></Header>
        <DraftActions />
        <VaDivider />
        <VaInnerLoading :loading="isLoading">
            <div style="min-height: 100vh">
                <VaForm ref="schemaForm">
                    <VaStepper @finish="submitProject" linear v-model="currentStep" :steps="steps">
                        <template #step-content-0>
                            <ProjectAttributes />
                        </template>
                        <template #step-content-1>
                            <ModelAttributes />
                        </template>
                        <template #step-content-2>
                            <StepSlot :model="'sample'" />
                        </template>
                        <template #step-content-3>
                            <StepSlot :model="'experiment'" />
                        </template>
                        <template #step-content-4>
                            <ResumeSlot />
                        </template>
                    </VaStepper>
                </VaForm>
            </div>
        </VaInnerLoading>
        <ConfirmOverwriteModal />
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { defineVaStepperSteps, useForm, useToast } from 'vuestic-ui'
import { useProjectStore } from '../../stores/project-store'
import ProjectService from '../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import Header from '../../components/ui/Header.vue'
import DraftActions from './components/actions/DraftActions.vue';
import StepSlot from './components/StepSlot.vue'
import ResumeSlot from './components/ResumeSlot.vue'
import ProjectAttributes from './components/attributes/ProjectAttributes.vue';
import ModelAttributes from './components/model/ModelAttributes.vue';
import { useRouter } from 'vue-router';
import ConfirmOverwriteModal from './components/ConfirmOverwriteModal.vue'

const title = 'Project form'
const description = 'Fill all the steps to create a new project, save it to draft at any moment'

const { init } = useToast()
const isLoading = ref(false)
const projectStore = useProjectStore()
const { validate } = useForm('schemaForm')
const router = useRouter()
const currentStep = ref(0)

const steps = ref(defineVaStepperSteps([
    {
        label: 'Project Info', beforeLeave: (step) => { step.hasError = !validate() }
    },
    {
        label: 'Model filters', beforeLeave: (step) => { step.hasError = !projectStore.currentProject.sample.fields.length }
    },
    {
        label: 'Sample Info', beforeLeave: (step) => { step.hasError = !isValidSample.value }
    },
    {
        label: 'Experiment Info', beforeLeave: (step) => { step.hasError = projectStore.currentProject.experiment.fields.length > 0 && !isValidExperiment.value }
    },
    {
        label: 'Review project', beforeLeave: async () => await submitProject()
    }
]))

const isValidSample = computed(() => {
    return projectStore.currentProject.sample.id_format.length > 0 && projectStore.currentProject.sample.fields.length > 0
})

const isValidExperiment = computed(() => {
    return projectStore.currentProject.experiment.id_format.length > 0 && projectStore.currentProject.experiment.fields.length > 0
})

async function submitProject() {
    isLoading.value = !isLoading.value
    try {
        const { data } = await ProjectService.createProject(projectStore.currentProject)
        data.forEach((d: string) => {
            init({ color: 'success', message: d })
        })
        projectStore.resetProject()
        projectStore.resetDraftProject()

        router.push({ name: 'projects' })
    } catch (error) {
        const axiosError = error as AxiosError
        console.log(axiosError)
        if (axiosError.response && axiosError.response.data) {
            const data = axiosError.response.data as string
            init({ color: 'danger', message: data })

        }
    } finally {
        isLoading.value = !isLoading.value
    }
}

</script>
