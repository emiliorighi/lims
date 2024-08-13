<template>
    <div class="row justify-space-between align-end">
        <h1 class="va-h1 flex pt-0">{{ title }}</h1>
        <div class="flex">
            <div class="row">
                <div v-for="c in actionsComponents" class="flex">
                    <component :is="c"></component>
                </div>
                <div class="flex">
                    <DownloadYAML :project="projectStore.currentProject" />
                </div>
            </div>
        </div>
    </div>
    <VaCard>
        <VaCardContent>
            <VaInnerLoading :loading="isLoading">
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
            </VaInnerLoading>
        </VaCardContent>
    </VaCard>
    <ConfirmOverwriteModal />
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { defineVaStepperSteps, useForm, useToast } from 'vuestic-ui'
import { useProjectStore } from '../../stores/project-store'
import ProjectService from '../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import SaveDraftProject from '../../components/buttons/SaveDraftProject.vue';
import UploadDraftProject from '../../components/buttons/UploadDraftProject.vue';
import UploadProject from '../../components/buttons/UploadProject.vue';
import DownloadYAML from '../../components/buttons/DownloadYAMLProject.vue';

import StepSlot from './steps/StepSlot.vue'
import ResumeSlot from './steps/ResumeSlot.vue'
import ProjectAttributes from './steps/ProjectAttributes.vue';
import ModelAttributes from './steps/ModelAttributes.vue';
import { useRouter } from 'vue-router';
import ConfirmOverwriteModal from '../../components/modals/ConfirmOverwriteModal.vue'

const title = 'Project Creation'

const actionsComponents = [SaveDraftProject, UploadDraftProject, UploadProject]
const { init } = useToast()
const isLoading = ref(false)
const projectStore = useProjectStore()
const { validate } = useForm('schemaForm')
const router = useRouter()
const currentStep = ref(0)

const steps = ref(defineVaStepperSteps([
    {
        label: 'Project', icon: 'folder', beforeLeave: (step) => { step.hasError = !validate() }
    },
    {
        label: 'Filters', icon: 'filter_list', beforeLeave: (step) => { step.hasError = !projectStore.currentProject.sample.fields.length }
    },
    {
        label: 'Sample', icon: 'fa-vial', beforeLeave: (step) => { step.hasError = !isValidSample.value }
    },
    {
        label: 'Experiment', icon: 'fa-dna', beforeLeave: (step) => { step.hasError = projectStore.currentProject.experiment.fields.length > 0 && !isValidExperiment.value }
    },
    {
        label: 'Resume', icon: 'check_circle', beforeLeave: async () => await submitProject()
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
