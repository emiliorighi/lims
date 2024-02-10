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
                                <va-input label="Project Identifier" :loading="isIdValidationLoading" readonly
                                    v-model="projectStore.project.project_id" :error="idAlreadyExists"></va-input>
                                <va-input
                                    :rules="[(v: string) => v.length > 3 || 'name is mandatory, at least 3 characters']"
                                    class="mt-4" label="name" v-model="projectStore.project.name" />
                                <va-input class="mt-4" label="version" v-model="projectStore.project.version"
                                    :rules="[(v: string) => v.length > 0 || 'version is mandatory']" />
                                <va-input class="mt-4" label="Project description"
                                    v-model="projectStore.project.description" />
                            </template>
                            <template #step-content-1>
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
                            <template #step-content-2>
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
                            <template #step-content-3>
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
import { computed, ref, watchEffect } from 'vue';
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

const { toast } = useGlobalStore()
const isLoading = ref(false)
const projectStore = useProjectStore()
const { validate } = useForm('schemaForm')

const isIdValidationLoading = ref(false)
const idAlreadyExists = ref(false)
const currentStep = ref(0)
const steps = ref(defineVaStepperSteps([
    {
        label: 'Project Info', beforeLeave: (step) => { step.hasError = !validate() }
    },
    {
        label: 'Sample Info', beforeLeave: (step) => { step.hasError = !isValidSample.value }
    },
    {
        label: 'Experiment Info', beforeLeave: (step) => { step.hasError = !isValidExperiment.value }
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

async function submitProject() {
    isLoading.value = !isLoading.value
    try {
        const { data } = await ProjectService.createProject(projectStore.project)
        data.forEach((d:Record<string,any>) => {
            toast({ color: 'success', message: d.message, duration: 1500 })
        })
        projectStore.resetProject()
    } catch (error) {
        const axiosError = error as AxiosError
        console.log(axiosError)
        if(axiosError.response && axiosError.response.data){
            const data = axiosError.response.data as Record<string,any>[]
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