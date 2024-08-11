<template>
    <VaInput readonly label="Unique identifier" v-model="id"
        placeholder="The unique identifier will be generated here" :rules="[rules]">
    </VaInput>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useSchemaStore } from './../../stores/schemas-store';
import { AxiosError } from 'axios';
import SampleService from './../../services/clients/SampleService';
import ExperimentService from './../../services/clients/ExperimentService';
import { useToast } from 'vuestic-ui/web-components';


const props = defineProps<{
    model: 'sample' | 'experiment',
    metadata: Record<string, any>
}>()

const schemaStore = useSchemaStore()

const { init } = useToast()

const modelExists = ref(false)

const isLoading = ref(false)

const rules = computed(() => {
    return [(v: string) => v.length > 0 || 'Fill the required fields to generate the unique identifier',
    !modelExists.value || `${props.model} already exists`]
})

const request = computed(() => {
    if (props.model === 'experiment') return ExperimentService.getExperiment

    return SampleService.getSample
})

const id = computed(() => {
    const keys = schemaStore.schema[props.model].id_format
    const values: string[] = [];

    for (const key of keys) {
        if (key in props.metadata) {
            values.push(String(props.metadata[key]));  // Ensure the value is a string
        } else {
            return '';  // Return false if any key is not found in the object
        }
    }
    // Join the values with an underscore
    return values.join('_');
})

watch(() => (id.value), async () => {
    if (!id.value) return

    await getItem(id.value)
})


async function getItem(id:string): Promise<void> {

    try {
        isLoading.value = true
        const response = await request.value(schemaStore.schema.project_id, id);
        const { data } = response;
        if (data) modelExists.value = true
        init({
            message: `${props.model} with ${id} already exists`,
            color: 'danger',
        });
    } catch (error) {
        if (error instanceof AxiosError) {
            if (error.response?.status !== 404) {
                // Sample is new

                console.error('Error:', error);
                init({
                    message: error.response?.data?.message,
                    color: 'danger',
                });
            } else {
                modelExists.value = false
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
</script>