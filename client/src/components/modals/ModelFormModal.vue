<template>
    <VaModal @cancel="emits('onCancel')" @ok="submit" max-height="500px" fixed-layout v-model="showForm">
        <template #header>
            <h3 class="va-h2">
                {{ idToUpdate ? `Update ${idToUpdate}` : `Create ${model}` }}
            </h3>
        </template>
        <VaDivider />
        <VaInnerLoading :loading="isLoading">
            <VaForm ref="modelForm">
                <div v-if="!idToUpdate" class="row">
                    <div class="flex lg6 md6 sm12 xs12">
                        <ModelID :model="model" :metadata="metadata"></ModelID>
                    </div>
                </div>
                <MetadataForm v-for="(f, index) in fields" :key="index" :existing-metadata="existingMetadata"
                    @update-field="updateModelField" :fields="f">
                </MetadataForm>
            </VaForm>
        </VaInnerLoading>
    </VaModal>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useForm, useToast } from 'vuestic-ui/web-components';
import { computed, ref } from 'vue';
import MetadataForm from '../forms/MetadataForm.vue'
import ModelID from '../forms/ModelID.vue'
import { ExperimentModel, Filter, SampleModel } from '../../data/types';
import SampleService from '../../services/clients/SampleService';
import ExperimentService from '../../services/clients/ExperimentService';

import { AxiosError } from 'axios';


const props = defineProps<{
    itemToEdit: SampleModel | ExperimentModel | undefined,
    showForm: boolean
    model: 'sample' | 'experiment',
}>()

const emits = defineEmits(['itemEdited', 'onCancel'])


const schemaStore = useSchemaStore()
const { init } = useToast()
const { validate } = useForm('modelForm')

const isLoading = ref(false)
const metadata = ref<Record<string, any>>({})

const existingMetadata = computed(() => {
    if (props.itemToEdit) return Object.entries(props.itemToEdit.metadata)
    return []
})

const idToUpdate = computed(() => {
    if (!props.itemToEdit) return undefined

    let itemID
    if (props.model === 'experiment') {
        const item = props.itemToEdit as ExperimentModel
        itemID = item.experiment_id
    } else {
        const item = props.itemToEdit as SampleModel
        itemID = item.sample_id
    }
    return itemID

})

const fields = computed(() => {
    const requiredFields = [] as Filter[]
    const optionalFields = [] as Filter[]
    const idFields = [] as Filter[]
    for (const f of schemaStore.schema[props.model].fields) {
        if (schemaStore.schema[props.model].id_format.includes(f.key)) {
            idFields.push(f)
        } else if (f.required) {
            requiredFields.push(f)
        } else {
            optionalFields.push(f)
        }
    }
    return [idFields, requiredFields, optionalFields].filter(a => a.length)
})

const submitItem = computed(() => {
    if (props.model === 'experiment') return ExperimentService.createExperiment
    return SampleService.createSample
})

const updateItem = computed(() => {
    if (props.model === 'experiment') return ExperimentService.updateExperiment
    return SampleService.updateSample
})


async function submit(): Promise<void> {
    if (!validate()) return
    try {

        isLoading.value = true
        if (idToUpdate.value) {
            const response = await updateItem.value(schemaStore.schema.project_id, idToUpdate.value, metadata.value);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `${props.model} ${idToUpdate.value} edited successfully`,
            });

        } else {
            const response = await submitItem.value(schemaStore.schema.project_id, metadata.value);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `${props.model} created successfully`,
            });

        }

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
        emits('onCancel')
    }
}

function updateModelField(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {

    metadata.value[tuple[0]] = tuple[1]

}


</script>