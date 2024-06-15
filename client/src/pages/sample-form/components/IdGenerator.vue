<template>
    <VaCard :loading="isLoading" stripe :stripe-color="color" square outlined>
        <VaCardContent style="padding-bottom: 0;" class="row align-center justify-space-between">
            <div class="flex">
                Fill the following fields <b>{{ schemaStore.schema.sample.id_format.join(', ') }}</b>
            </div>
            <div class="flex">
                <VaButton :color="color" :icon="icon" rounded />
            </div>
        </VaCardContent>
        <VaDivider/>
        <VaAlert color="danger" v-if="sampleExists">A sample with ID:{{ id }} already exists</VaAlert>
        <VaCardContent>
            <h4 style="margin-top: 0;" class="va-h4">Sample ID: {{ id ? id : '' }}</h4>
            <p v-if="id" class="va-text-success">The sample Id is valid</p>
            <p v-else class="va-text-danger">The sample Id is not valid</p>
        </VaCardContent>
        <VaInput v-if="id" style="display:none" class="flex lg8 md8" readonly label="Unique identifier" v-model="id"
            placeholder="The unique identifier will be generated here"
            :rules="[requiredIdRule, !sampleExists || 'Sample Id already exists']">
        </VaInput>
    </VaCard>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useSampleStore } from '../../../stores/sample-store';
import { useSchemaStore } from '../../../stores/schemas-store';
import { AxiosError } from 'axios';
import SampleService from '../../../services/clients/SampleService';
import { useToast } from 'vuestic-ui/web-components';

const schemaStore = useSchemaStore()

const { init } = useToast()

const sampleStore = useSampleStore()

const sampleExists = ref(false)

const isLoading = ref(false)

const id = ref<string | false>(false)
// map the ordered list of id fields then set by order the value in the name

const requiredIdRule = (v: string) => v.length > 0 || 'Fill the required fields to generate the unique identifier'

const color = computed(() => {
    return id.value ? 'success' : 'danger'
})
const icon = computed(() => {
    return id.value ? 'verified' : 'dangerous'
})


watch(() => (Object.entries(sampleStore.sample.metadata)), async () => {

    if (!sampleStore.sample.metadata) return

    const genId = generateId(schemaStore.schema.sample.id_format, sampleStore.sample.metadata)

    if (!genId) return

    if (genId === id.value) return

    id.value = genId

    await getSample(id.value)
})

function generateId(keys: string[], obj: Record<string, any>): string | false {
    // Use an array to collect values
    const values: string[] = [];

    for (const key of keys) {
        if (key in obj) {
            values.push(String(obj[key]));  // Ensure the value is a string
        } else {
            return false;  // Return false if any key is not found in the object
        }
    }
    // Join the values with an underscore
    return values.join('_');
}

async function getSample(id: string): Promise<void> {

    try {
        isLoading.value = true
        const response = await SampleService.getSample(schemaStore.schema.project_id, id);
        const { data } = response;
        if (data) sampleExists.value = true
        init({
            message: `Sample ${id} already exists`,
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
                sampleExists.value = false
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