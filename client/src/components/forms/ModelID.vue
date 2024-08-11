<template>
    <VaInput class="flex" readonly label="Unique identifier" v-model="id"
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
    id: string
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

watch(() => (props.id), async () => {
    if (!props.id) return

    await getModel()
})


async function getModel(): Promise<void> {

    try {
        isLoading.value = true
        const response = await request.value(schemaStore.schema.project_id, props.id);
        const { data } = response;
        if (data) modelExists.value = true
        init({
            message: `${props.model} with ${props.id} already exists`,
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