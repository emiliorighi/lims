<template>
    <VaModal @cancel="experimentStore.expIdToUpdate = undefined" max-height="500px" fixed-layout
        v-model="experimentStore.showForm" hide-default-actions>
        <template #header>
            <h3 class="va-h3">
                {{ experimentStore.expIdToUpdate ? `Update ${experimentStore.expIdToUpdate}` : 'Create experiment' }}
            </h3>
        </template>
        <VaDivider />
        <VaInnerLoading :loading="isLoading">
            <VaForm ref="experimentForm">
                <div class="row">
                    <div v-for="step in steps" class="flex lg12 md12 sm12 xs12">
                        <h4 class="va-h4">{{ step.label }}</h4>
                        <p class="va-text-secondary">{{ step.description }} </p>
                        <IdGenerator v-if="step.label === 'Id Fields'" />
                        <MetadataForm :existing-metadata="existingMetadata" @update-field="updateexperimentField"
                            :fields="step.fields"></MetadataForm>
                    </div>
                </div>
            </VaForm>
        </VaInnerLoading>
        <VaDivider />
        <template #footer>
            <VaCardActions align="end">
                <VaButton @click="submitExperiment">Submit</VaButton>
            </VaCardActions>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../../stores/schemas-store';
import { VaModal, useForm, useToast } from 'vuestic-ui/web-components';
import { computed, onMounted, ref } from 'vue';
import MetadataForm from './../../../components/forms/MetadataForm.vue'
import IdGenerator from './IdGenerator.vue'
import { Filter } from '../../../data/types';
import { AxiosError } from 'axios';
import { Step } from 'vuestic-ui/dist/types/components/va-stepper/types';
import { useExperimentStore } from '../../../stores/experiment-store';
import ExperimentService from '../../../services/clients/ExperimentService';

const schemaStore = useSchemaStore()
const experimentStore = useExperimentStore()
const { init } = useToast()
const { validate } = useForm('experimentForm')

const emits = defineEmits(['experimentEdited'])
const requiredFields = ref<Filter[]>([])
const optionalFields = ref<Filter[]>([])
const idFields = ref<Filter[]>([])
const isLoading = ref(false)

const existingMetadata = computed(() => {
    if (experimentStore.experiment === null) return undefined
    return Object.entries(experimentStore.experiment.metadata)
})

const steps = computed(() => {
    const validSteps = []
    if (idFields.value.length && !experimentStore.expIdToUpdate) {
        validSteps.push(
            {
                label: 'Id Fields',
                description: 'Mandatory fields used to generate the experiment Id, fill them by order',
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

    if (experimentStore.expIdToUpdate) {
        await getExperiment(experimentStore.expIdToUpdate)
    }
})


async function getExperiment(id: string): Promise<void> {

    try {
        isLoading.value = true
        const response = await ExperimentService.getExperiment(schemaStore.schema.project_id, id);
        const { data } = response;
        experimentStore.experiment = { ...data }
    } catch (error) {
        if (error instanceof AxiosError) {
            if (error.response?.status === 404) {
                console.error('Error:', error);
                init({
                    message: `experiment with Id: ${id} not found!`,
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
    for (const f of schemaStore.schema.experiment.fields) {
        if (schemaStore.schema.experiment.id_format.includes(f.key)) {
            idFields.value.push(f)
        } else if (f.required) {
            requiredFields.value.push(f)
        } else {
            optionalFields.value.push(f)
        }
    }
}

async function submitExperiment(): Promise<void> {
    if (!validate()) return
    try {

        isLoading.value = true
        const { metadata, sample_id } = experimentStore.experiment
        if (experimentStore.expIdToUpdate) {
            const response = await ExperimentService.updateExperiment(schemaStore.schema.project_id, experimentStore.expIdToUpdate, metadata);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `experiment ${experimentStore.expIdToUpdate} edited successfully`,
            });

        } else {
            const response = await ExperimentService.createExperiment(schemaStore.schema.project_id, { ...metadata, sample_id });
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : 'experiment created successfully',
            });

        }

        experimentStore.showForm = !experimentStore.showForm
        emits('experimentEdited')
        // router.push({ name: 'experiments', params: { projectId: schemaStore.schema.project_id } })

    } catch (error) {
        console.error('Error creating experiment:', error);

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

function updateexperimentField(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {

    experimentStore.experiment.metadata[tuple[0]] = tuple[1]

}

</script>