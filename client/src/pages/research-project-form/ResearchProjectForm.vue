<template>
    <div>
        <Header :title="title" />
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <VaInnerLoading :loading="isLoading">
                    <VaForm ref="schemaForm">
                        <VaStepper color="textPrimary" @finish="submitProject" linear v-model="currentStep"
                            :steps="steps">
                            <template #step-content-0>
                                <ProjectAttributes />
                            </template>
                            <template #step-content-1>
                                <ReferenceModels />
                            </template>
                            <template #step-content-2>
                                <ResumeSlot />
                            </template>
                        </VaStepper>
                    </VaForm>
                </VaInnerLoading>
            </div>
        </div>
    </div>

</template>
<script setup lang="ts">
import { ref } from 'vue';
import { defineVaStepperSteps, useForm, useToast } from 'vuestic-ui'
import { useProjectStore } from '../../stores/project-store'
import { AxiosError } from 'axios';
import ResumeSlot from './steps/ResumeSlot.vue'
import ProjectAttributes from './steps/ProjectAttributes.vue';
import { useRouter } from 'vue-router';
import Header from '../../components/ui/Header.vue'
import AuthService from '../../services/clients/AuthService';
import ReferenceModels from './steps/Models.vue';

const props = defineProps<{
    title: string
}>()

const { init } = useToast()
const isLoading = ref(false)
const projectStore = useProjectStore()
const router = useRouter()
const currentStep = ref(0)
const { validate } = useForm('schemaForm')

const steps = ref(defineVaStepperSteps([
    {
        label: 'Project Information',
        beforeLeave: (step) => {
            step.hasError = !validate() || projectStore.projectIdExists
        }
    },
    {
        label: 'Models',
        beforeLeave: (step) => { step.hasError = !validate() },
    },
    {
        label: 'Review',
    }
]))


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
