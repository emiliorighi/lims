<template>
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <va-card :loading="isLoading" style="min-height: 100vh">
                <va-card-title>
                    Project Creation Form
                </va-card-title>
                <DraftActions />
                <va-card-content>
                    <va-form ref="schemaForm">
                        <va-stepper @finish="submitProject" linear v-model="currentStep" :steps="steps">
                            <template #step-content-0>
                                <ProjectAttributes />
                            </template>
                            <template #step-content-1>
                                <ModelAttributes/>
                            </template>
                            <template #step-content-2>
                                <div class="step-slot">
                                    <div class="row row-equal">
                                        <div class="flex lg12 md12 sm12 xs12">
                                            <IdFieldsCard :model="'sample'" />
                                        </div>
                                    </div>
                                    <div class="row row-equal">
                                        <div class="flex lg12 md12 sm12 xs12">
                                            <AttributeCRUDTable :model="'sample'" />
                                        </div>
                                    </div>
                                </div>
                            </template>
                            <template #step-content-3>
                                <div class="step-slot">
                                    <div class="row row-equal">
                                        <div class="flex lg12 md12 sm12 xs12">
                                            <IdFieldsCard :model="'experiment'" />
                                        </div>
                                    </div>
                                    <div class="row row-equal">
                                        <div class="flex lg12 md12 sm12 xs12">
                                            <AttributeCRUDTable :model="'experiment'" />
                                        </div>
                                    </div>
                                </div>
                            </template>
                            <template #step-content-4>
                                <h2 class="va-h2"> Resume of {{ projectStore.project.project_id }}
                                </h2>
                                <div class="row row-equal">
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <ProjectOverviewCard :metadata="projectStore.project" />
                                    </div>
                                </div>
                            </template>
                        </va-stepper>
                    </va-form>
                </va-card-content>
            </va-card>
            <DraftActionModal />
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { defineVaStepperSteps, useForm } from 'vuestic-ui'
import { useProjectStore } from '../../stores/project-store'
import ProjectService from '../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import DraftActions from './components/DraftActions.vue'
import DraftActionModal from './components/DraftActionModal.vue'
import IdFieldsCard from './components/IdFieldsCard.vue';
import AttributeCRUDTable from './components/AttributeCRUDTable.vue';
import ProjectOverviewCard from './components/ProjectOverviewCard.vue';
import { useGlobalStore } from '../../stores/global-store';
import ProjectAttributes from './components/ProjectAttributes.vue';
import ModelAttributes from './components/ModelAttributes.vue';
import { useRouter } from 'vue-router';
const { toast } = useGlobalStore()
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
        label: 'Model Attributes', beforeLeave: (step) => { step.hasError = !projectStore.project.sample.fields.length }
    },
    {
        label: 'Sample Info', beforeLeave: (step) => { step.hasError = !isValidSample.value }
    },
    {
        label: 'Experiment Info', beforeLeave: (step) => { step.hasError = projectStore.project.experiment.fields.length > 0 && !isValidExperiment.value }
    },
    {
        label: 'Review project', beforeLeave: async () => await submitProject()
    }
]))

const isValidSample = computed(() => {
    return projectStore.project.sample.id_format.length > 0 && projectStore.project.sample.fields.length > 0
})
const isValidExperiment = computed(() => {
    return projectStore.project.experiment.id_format.length > 0 && projectStore.project.experiment.fields.length > 0
})

async function submitProject() {
    isLoading.value = !isLoading.value
    try {
        const { data } = await ProjectService.createProject(projectStore.project)
        console.log(data)
        data.forEach((d: Record<string, any>) => {
            toast({ color: 'success', message: d.message, duration: 1500 })
        })
        router.push({name: 'projects'})
        // projectStore.resetProject()
    } catch (error) {
        const axiosError = error as AxiosError
        console.log(axiosError)
        if (axiosError.response && axiosError.response.data) {
            const data = axiosError.response.data as Record<string, any>[]
            data.forEach((d) => {
                toast({ color: 'danger', message: d.message })
            })
        }
    } finally {
        isLoading.value = !isLoading.value
    }
}

</script>
<style scoped>
.step-slot {
    min-height: 60vh;
}
</style>