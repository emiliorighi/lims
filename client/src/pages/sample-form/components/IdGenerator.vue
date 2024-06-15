<template>
    <div class="row">
        <VaInput class="flex lg6 md6 sm12 xs12" readonly label="Unique identifier" v-model="id" placeholder="The unique identifier will be generated here"
            :rules="[requiredIdRule, !sampleExists || 'Sample Id already exists']">
        </VaInput>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
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

const id = ref<string>('')
// map the ordered list of id fields then set by order the value in the name

const requiredIdRule = (v: string) => v.length > 0 || 'Fill the required fields to generate the unique identifier'

onMounted(async () => {
    await triggerIdCheck()
})

watch(() => (Object.entries(sampleStore.sample.metadata)), async () => {
    await triggerIdCheck()
})

async function triggerIdCheck() {

    if (!sampleStore.sample.metadata) return

    const genId = generateId(schemaStore.schema.sample.id_format, sampleStore.sample.metadata)

    if (!genId) return

    if (genId === id.value) return

    id.value = genId

    await getSample(id.value)
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