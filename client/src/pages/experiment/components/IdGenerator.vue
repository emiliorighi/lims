<template>
    <div class="row">
        <VaInput class="flex" readonly label="Unique identifier" v-model="id"
            placeholder="The unique identifier will be generated here"
            :rules="[requiredIdRule, !expExists || 'Experiment Id already exists']">
        </VaInput>
    </div>
    <div class="row">
        <VaSelect class="flex" :rules="[(v: string) => !!v || 'Sample is mandatory']" @update:search="handleSearch"
            v-model="experimentStore.experiment.sample_id" :options="samples" label="Sample" :loading="isLoading"
            dropdownIcon="search" searchable highlight-matched-text searchPlaceholderText="Type to search"
            noOptionsText="No sample found">
        </VaSelect>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useSchemaStore } from '../../../stores/schemas-store';
import { AxiosError } from 'axios';
import ExperimentService from '../../../services/clients/ExperimentService';
import { useToast } from 'vuestic-ui/web-components';
import { useExperimentStore } from '../../../stores/experiment-store';
import SampleService from '../../../services/clients/SampleService';
import { SampleModel } from '../../../data/types';

const schemaStore = useSchemaStore()

const { init } = useToast()

const experimentStore = useExperimentStore()

const expExists = ref(false)

const isLoading = ref(false)

const sampleId = ref('')

const samples = ref<string[]>([])
const id = ref<string>('')
// map the ordered list of id fields then set by order the value in the name

const requiredIdRule = (v: string) => v.length > 0 || 'Fill the required fields to generate the unique identifier'

onMounted(async () => {
    await triggerIdCheck()
})

watch(() => (Object.entries(experimentStore.experiment.metadata)), async () => {
    await triggerIdCheck()
})

async function triggerIdCheck() {

    if (!experimentStore.experiment.metadata) return

    const genId = generateId(schemaStore.schema.experiment.id_format, experimentStore.experiment.metadata)

    if (!genId) return

    if (genId === id.value) return

    id.value = genId

    await getExperiment(id.value)
}

function generateId(keys: string[], obj: Record<string, any>): string | false {
    // Use an array to collect values
    const values: string[] = [];

    for (const key of keys) {
        if (key in obj) {
            values.push(String(obj[key]));  // Ensure the value is a string
        } else {
            return '';  // Return false if any key is not found in the object
        }
    }
    // Join the values with an underscore
    return values.join('_');
}

async function getExperiment(id: string): Promise<void> {

    try {
        isLoading.value = true
        const response = await ExperimentService.getExperiment(schemaStore.schema.project_id, id);
        const { data } = response;
        if (data) expExists.value = true
        init({
            message: `Experiment ${id} already exists`,
            color: 'danger',
        });
    } catch (error) {
        if (error instanceof AxiosError) {
            if (error.response?.status !== 404) {

                console.error('Error:', error);
                init({
                    message: error.response?.data?.message,
                    color: 'danger',
                });
            } else {
                expExists.value = false
            }
        } else {
            console.error('Unexpected error:', error);
            init({
                message: 'An unexpected error occurred',
                color: 'danger',
            });
        }
    } finally {
        isLoading.value = true
    }
}

async function handleSearch(v: string) {
    if (v.length < 2) return
    isLoading.value = true
    try {
        const { data } = await SampleService.getSamples(schemaStore.schema.project_id, { filter: v })
        samples.value = [...data.data.map((d: SampleModel) => d.sample_id)]
    } catch (error) {
        const axiosError = error as AxiosError
        init({ message: axiosError.message, color: 'danger' })
    } finally {
        isLoading.value = false
    }
}
</script>