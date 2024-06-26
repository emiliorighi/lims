<template>
    <div>
        <h1 class="va-h1">{{ experimentId }}</h1>
        <p style="margin-bottom: 6px" class="va-text-secondary"> Experiment of {{ projectId }}</p>
        <VaDivider/>
        <div v-if="sample" class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <MetadataTree :metadata="Object.entries(sample.metadata)" />
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import ProjectService from '../../services/clients/ProjectService';
import ExperimentService from '../../services/clients/ExperimentService';
import { useToast } from 'vuestic-ui/web-components';
import { AxiosError } from 'axios';
import { SampleModel } from '../../data/types';
import MetadataTree from '../../components/data/MetadataTree.vue';


const schemaStore = useSchemaStore()
const isLoading = ref(false)
const { init } = useToast()

const props = defineProps<{
    projectId: string
    experimentId: string
}>()

const sample = ref<SampleModel>()

onMounted(async () => {

    if (!schemaStore.schema.project_id) {
        await fetchSchema(props.projectId)
    }

    await fetchExperiment(props.projectId, props.experimentId)
})


async function fetchSchema(projectId: string) {
    try {
        isLoading.value = true
        const { data } = await ProjectService.getProject(projectId)
        schemaStore.schema = { ...data }
    } catch (e) {
        let message: string
        const axiosError = e as AxiosError

        if (axiosError.response?.data) {
            message = (axiosError.response.data as { message: string }).message || axiosError.response.data as string
        } else {
            message = axiosError.message
        }

        init({ message: message, color: 'danger' })
    } finally {
        isLoading.value = false
    }
}

async function fetchExperiment(projectId: string, experimentId: string) {
    try {
        isLoading.value = true
        const { data } = await ExperimentService.getExperiment(projectId, experimentId)
        sample.value = { ...data }
    } catch (e) {
        let message: string
        const axiosError = e as AxiosError

        if (axiosError.response?.data) {
            message = (axiosError.response.data as { message: string }).message || axiosError.response.data as string
        } else {
            message = axiosError.message
        }

        init({ message: message, color: 'danger' })
    } finally {
        isLoading.value = false
    }

}

</script>