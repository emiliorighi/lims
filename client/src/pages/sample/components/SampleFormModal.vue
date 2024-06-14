<template>
    <div>
        <VaModal hide-default-actions class="modal-crud" :model-value="sampleStore.showForm" @cancel="reset">
            <template #header>
                <h2 class="va-h2">
                    {{ sampleStore.isUpdate ? `Editing Sample ${sampleStore.sample?.sample_id}` : 'Creating Sample' }}
                </h2>
            </template>
            <ItemForm @on-metadata-valid="validateSample" @on-reset="reset"
                :existing-metadata="Object.entries(sampleStore.sample?.metadata || {})"
                :fields="(schema.sample.fields as Filter[])" :id_format="(schema.sample.id_format as string[])" />
        </VaModal>
        <VaModal hide-default-actions :model-value="!!existingSample">
            <template #header>
                <h2 class="va-h2">
                    Sample {{ existingSample?.sample_id }} already exists!
                </h2>
            </template>
            <VaDivider />
            <div class="row justify-space-between">
                <div class="flex">
                    <VaButton @click="updateSample" color="warning">Overwrite</VaButton>
                </div>
                <div class="flex">
                    <VaButton @click="existingSample = undefined" color="secondary">Return</VaButton>
                </div>
            </div>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../../stores/schemas-store';
import { useSampleStore } from '../../../stores/sample-store';
import { Filter, SampleModel } from '../../../data/types'
import { ref } from 'vue';
import SampleService from '../../../services/clients/SampleService'
import { useGlobalStore } from '../../../stores/global-store';
import { AxiosError } from 'axios';
import ItemForm from '../../../components/forms/ItemForm.vue'

const emits = defineEmits(['onSampleEdited'])
const { schema } = useSchemaStore()
const sampleStore = useSampleStore()
const existingSample = ref<SampleModel>()

const { toast } = useGlobalStore()

async function updateSample(): Promise<void> {
    if (!existingSample.value) return;

    try {
        const response = await SampleService.updateSample(
            schema.project_id,
            existingSample.value.sample_id,
            existingSample.value.metadata
        );
        const { data } = response;

        toast({
            color: 'success',
            message: Array.isArray(data) ? data.join(', ') : 'Sample updated successfully',
        });

        reset();
        emits('onSampleEdited');
        existingSample.value = undefined;
    } catch (error) {
        console.error('Error updating sample:', error);

        let message = 'Impossible to update';
        if (error instanceof AxiosError) {
            message = error.response?.data?.message || message;
        }

        toast({
            color: 'danger',
            message,
        });
    }
}

async function createSample(formData: Record<string, any>): Promise<void> {
    try {
        const response = await SampleService.createSample(schema.project_id, formData);
        const { data } = response;

        toast({
            color: 'success',
            message: Array.isArray(data) ? data.join(', ') : 'Sample created successfully',
        });
        reset();
        emits('onSampleEdited');
    } catch (error) {
        console.error('Error creating sample:', error);

        let message = 'Impossible to save';
        if (error instanceof AxiosError) {
            message = error.response?.data?.message || message;
        }

        toast({
            color: 'danger',
            message,
        });
    }
}

async function validateSample(metadata: Record<string, any>): Promise<void> {
    const id = Object.entries(metadata)
        .filter(([key]) => schema.sample.id_format.includes(key))
        .map(([, value]) => value)
        .join('_');

    try {
        const response = await SampleService.getSample(schema.project_id, id);
        const { data } = response;
        existingSample.value = { ...data }
        if (existingSample.value?.metadata) {
            existingSample.value.metadata = { ...metadata }
        }

    } catch (error) {
        existingSample.value = undefined;

        if (error instanceof AxiosError) {
            if (error.response?.status === 404) {
                // Sample is new
                await createSample(metadata);
            } else {
                console.error('Error validating sample:', error);
                toast({
                    message: error.response?.data?.message || 'Error occurred while validating',
                    color: 'danger',
                });
            }
        } else {
            console.error('Unexpected error:', error);
            toast({
                message: 'An unexpected error occurred',
                color: 'danger',
            });
        }
    }
}


function reset() {
    sampleStore.sample = null
    sampleStore.showForm = !sampleStore.showForm
}
</script>
