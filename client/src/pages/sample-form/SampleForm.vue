<template>
    <div>
        <Header :title="title" :description="description"></Header>
        <VaDivider style="margin-top: 0;" />
        <VaInnerLoading :loading="isLoading">
            <div style="min-height: 100vh">
                <VaForm ref="sampleForm">
                    <div class="row">
                        <div class="flex lg6 md6 sm12 xs12">
                            <IdGenerator />
                        </div>
                    </div>
                    <div v-for="f in [
            { label: 'Id', description: 'Mandatory fields used to generate the sample Id, fill them by order', fields: idFields },
            { label: 'Required', description: 'Mandatory fields', fields: requiredFields },
            { label: 'Optional', description: 'Optional fields', fields: optionalFields }
        ]
            .filter(f => f.fields.length)" :key="f.label">
                        <div class="row">
                            <div class="flex lg8 md8 sm12 xs12">
                                <VaCard>
                                    <VaCardContent>
                                        <h4 class="va-h4">{{ f.label }} Fields</h4>
                                        <p class="va-text-secondary">{{ f.description }} </p>
                                    </VaCardContent>
                                    <VaDivider/>
                                    <VaCardContent>
                                        <MetadataForm :existing-metadata="existingMetadata"
                                            @update-field="updateSampleField" :fields="f.fields"></MetadataForm>
                                    </VaCardContent>
                                </VaCard>
                            </div>
                        </div>
                    </div>
                </VaForm>
            </div>
        </VaInnerLoading>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useSampleStore } from '../../stores/sample-store';
import { useToast } from 'vuestic-ui/web-components';
import { computed, onMounted, ref } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import MetadataForm from './components/MetadataForm.vue'
import IdGenerator from './components/IdGenerator.vue'
import { Filter } from '../../data/types';
import Header from '../../components/ui/Header.vue';
import SampleService from '../../services/clients/SampleService';
import { AxiosError } from 'axios';

const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { init } = useToast()


const props = defineProps<{
    sampleId?: string
    projectId: string
}>()

const requiredFields = ref<Filter[]>([])
const optionalFields = ref<Filter[]>([])
const idFields = ref<Filter[]>([])
const isLoading = ref(false)

const title = 'Sample form'
const description = 'Fill all the steps to create a new sample'

const existingMetadata = computed(() => {
    if (sampleStore.sample === null) return undefined
    return Object.entries(sampleStore.sample.metadata)
})

onMounted(async () => {

    if (!schemaStore.schema.project_id) {
        await fetchSchema(props.projectId)
    }

    mapFields()

    if (props.sampleId && sampleStore.sample === null) {
        await getSample(props.sampleId)
    }
})

async function fetchSchema(projectId: string) {
    try {
        isLoading.value = true
        const { data } = await ProjectService.getProject(projectId)
        schemaStore.schema = {
            ...data
        }
    } catch (error) {
        console.error(error)
        init({ message: 'Error fetching project..', color: 'danger', duration: 1500 })
    } finally {
        isLoading.value = false
    }
}
async function getSample(id: string): Promise<void> {

    try {
        isLoading.value = true
        const response = await SampleService.getSample(schemaStore.schema.project_id, id);
        const { data } = response;
        sampleStore.sample = { ...data }
    } catch (error) {
        if (error instanceof AxiosError) {
            if (error.response?.status === 404) {
                console.error('Error:', error);
                init({
                    message: `Sample with Id: ${id} not found!`,
                    color: 'danger',
                });
            } else {
                init({
                    message: error.response?.data.message,
                    color: 'danger',
                });
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
function mapFields() {
    for (const f of schemaStore.schema.sample.fields) {
        if (schemaStore.schema.sample.id_format.includes(f.key)) {
            idFields.value.push(f)
        } else if (f.required) {
            requiredFields.value.push(f)
        } else {
            optionalFields.value.push(f)
        }
    }
}

function updateSampleField(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {

    sampleStore.sample.metadata[tuple[0]] = tuple[1]

}

</script>