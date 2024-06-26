<template>
    <div>
        <Header :title="header.title" :description="header.description"></Header>
        <VaDivider style="margin-top: 0;" />
        <VaInnerLoading :loading="isLoading">
            <VaForm ref="sampleForm">
                <VaStepper @finish="submitSample" v-if="steps.length" v-model="step" :steps="steps" linear>
                    <template v-for="(step, i) in steps" :key="step.label" #[`step-content-${i}`]>
                        <div class="row">
                            <VaCard class="flex lg12 md12 sm12 xs12">
                                <VaCardContent>
                                    <h4 class="va-h4">{{ step.label }}</h4>
                                    <p class="va-text-secondary">{{ step.description }} </p>
                                </VaCardContent>
                                <VaDivider />
                                <VaCardContent v-if="step.label === 'Id Fields'">
                                    <IdGenerator />
                                </VaCardContent>
                                <VaCardContent style="height: 300px;overflow: scroll;">
                                    <MetadataForm :existing-metadata="existingMetadata"
                                        @update-field="updateSampleField" :fields="step.fields"></MetadataForm>
                                </VaCardContent>
                            </VaCard>
                        </div>
                    </template>
                </VaStepper>
            </VaForm>
        </VaInnerLoading>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useSampleStore } from '../../stores/sample-store';
import { useForm, useToast } from 'vuestic-ui/web-components';
import { computed, onMounted, ref } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import MetadataForm from './components/MetadataForm.vue'
import IdGenerator from './components/IdGenerator.vue'
import { Filter } from '../../data/types';
import Header from '../../components/ui/Header.vue';
import SampleService from '../../services/clients/SampleService';
import { AxiosError } from 'axios';
import { Step } from 'vuestic-ui/dist/types/components/va-stepper/types';
import { useRouter } from 'vue-router';


const step = ref(0)

const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { init } = useToast()
const { validate } = useForm('sampleForm')

const props = defineProps<{
    sampleId?: string
    projectId: string
}>()

const router = useRouter()
const requiredFields = ref<Filter[]>([])
const optionalFields = ref<Filter[]>([])
const idFields = ref<Filter[]>([])
const isLoading = ref(false)




const header = computed(() => {
    const title = 'Sample form'
    const projectTest = ` for Project ${props.projectId}`
    const description = 'Fill all the steps to create a new sample' + projectTest
    if (props.sampleId) return { title: `Sample form of ${props.sampleId}`, description: 'Fill all the steps to update the sample' + ' ' + props.sampleId + projectTest }
    return { title, description }
})
const existingMetadata = computed(() => {
    if (sampleStore.sample === null) return undefined
    return Object.entries(sampleStore.sample.metadata)
})

const steps = computed(() => {
    const validSteps = []
    if (idFields.value.length && !props.sampleId) {
        validSteps.push(
            {
                label: 'Id Fields',
                description: 'Mandatory fields used to generate the sample Id, fill them by order',
                fields: [...idFields.value],
                beforeLeave: (step: Step) => { step.hasError = !validate() }
            })
    }
    if (requiredFields.value.length) {
        validSteps.push(
            {
                label: 'Required Fields',
                description: 'Fill all the required fields',
                fields: [...requiredFields.value],
                beforeLeave: (step: Step) => { step.hasError = !validate() }
            }
        )
    }
    if (optionalFields.value.length) {
        validSteps.push(
            {
                label: 'Optional Fields',
                description: 'Optionally fill this fields',
                fields: [...optionalFields.value]
            }
        )
    }
    return validSteps
})
onMounted(async () => {

    if (!schemaStore.schema.project_id) {
        await fetchSchema(props.projectId)
    }

    mapFields()

    if (props.sampleId) {
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
        isLoading.value = false
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

async function submitSample(): Promise<void> {
    try {

        isLoading.value = true
        const { metadata } = sampleStore.sample
        if (props.sampleId) {
            const response = await SampleService.updateSample(schemaStore.schema.project_id, props.sampleId, metadata);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `Sample ${props.sampleId} edited successfully`,
            });

        } else {
            const response = await SampleService.createSample(schemaStore.schema.project_id, metadata);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : 'Sample created successfully',
            });

        }

        router.push({ name: 'samples', params: { projectId: schemaStore.schema.project_id } })

    } catch (error) {
        console.error('Error creating sample:', error);

        let message = 'Impossible to save';
        if (error instanceof AxiosError) {
            message = error.response?.data?.message || message;
        }
        init({
            color: 'danger',
            message,
        });
    } finally {
        isLoading.value = false
    }
}

function updateSampleField(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {

    sampleStore.sample.metadata[tuple[0]] = tuple[1]

}

</script>