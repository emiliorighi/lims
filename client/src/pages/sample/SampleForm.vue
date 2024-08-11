<template>
    <div>
        <template #header>
            <h3 class="va-h3">
                {{ sampleStore.sampleIdToUpdate ? `Update ${sampleStore.sampleIdToUpdate}` : 'Create Sample' }}
            </h3>
        </template>
        <VaDivider />
        <VaInnerLoading :loading="isLoading">
            <VaForm ref="sampleForm">
                <div class="row">
                    <div v-for="step in steps" class="flex lg12 md12 sm12 xs12">
                        <h4 class="va-h4">{{ step.label }}</h4>
                        <p class="va-text-secondary">{{ step.description }} </p>
                        <IdGenerator v-if="step.label === 'Id Fields'" />
                        <MetadataForm :existing-metadata="existingMetadata" @update-field="updateSampleField"
                            :fields="step.fields"></MetadataForm>
                    </div>
                </div>
            </VaForm>
        </VaInnerLoading>
        <VaDivider />
        <template #footer>
            <VaCardActions align="end">
                <VaButton @click="submitSample">Submit</VaButton>
            </VaCardActions>
        </template>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useSampleStore } from '../../stores/sample-store';
import { VaModal, useForm, useToast } from 'vuestic-ui/web-components';
import { computed, onMounted, ref } from 'vue';
import MetadataForm from './../../components/forms/MetadataForm.vue'
import IdGenerator from './components/IdGenerator.vue'
import { Filter } from '../../data/types';
import SampleService from '../../services/clients/SampleService';
import { AxiosError } from 'axios';
import { Step } from 'vuestic-ui/dist/types/components/va-stepper/types';

const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { init } = useToast()
const { validate } = useForm('sampleForm')

const emits = defineEmits(['sampleEdited'])
const requiredFields = ref<Filter[]>([])
const optionalFields = ref<Filter[]>([])
const idFields = ref<Filter[]>([])
const isLoading = ref(false)

const existingMetadata = computed(() => {
    if (sampleStore.sample === null) return undefined
    return Object.entries(sampleStore.sample.metadata)
})

const steps = computed(() => {
    const validSteps = []
    if (idFields.value.length && !sampleStore.sampleIdToUpdate) {
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


    mapFields()

    if (sampleStore.sampleIdToUpdate) {
        await getSample(sampleStore.sampleIdToUpdate)
    }
})


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
    if (!validate()) return
    try {

        isLoading.value = true
        const { metadata } = sampleStore.sample
        if (sampleStore.sampleIdToUpdate) {
            const response = await SampleService.updateSample(schemaStore.schema.project_id, sampleStore.sampleIdToUpdate, metadata);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `Sample ${sampleStore.sampleIdToUpdate} edited successfully`,
            });

        } else {
            const response = await SampleService.createSample(schemaStore.schema.project_id, metadata);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : 'Sample created successfully',
            });

        }

        sampleStore.showForm = !sampleStore.showForm
        emits('sampleEdited')
        // router.push({ name: 'samples', params: { projectId: schemaStore.schema.project_id } })

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