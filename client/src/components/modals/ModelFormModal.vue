<template>
    <VaModal hide-default-actions max-height="500px" fixed-layout v-model="schemaStore.showForm">
        <template #header>
            <h3 class="va-h3">
                {{ idToUpdate ? `Update ${idToUpdate}` : `Create ${schemaStore.model}` }}
            </h3>
        </template>
        <VaDivider />
        <VaInnerLoading :loading="isLoading">
            <VaForm ref="modelForm">
                <div v-if="!idToUpdate">
                    <div>
                        <h6 class="va-h6">Generated ID</h6>
                        <p class="va-text-secondary mb-2">This section displays the generated ID</p>
                        <div class="row">
                            <div class="flex lg6 md6 sm12 xs12 mb-2">
                                <ModelID :model="schemaStore.model" :metadata="metadata"></ModelID>
                            </div>
                        </div>
                    </div>
                    <div v-if="schemaStore.model === 'experiment'">
                        <h6 class="va-h6">Sample Linking</h6>
                        <p class="va-text-secondary mb-2">Link this experiment to a sample </p>
                        <div class="row">
                            <VaSelect class="flex lg6 md6 sm12 xs12 mb-2"
                                :rules="[(v: string) => !!v || 'Sample is mandatory']" @update:search="handleSearch"
                                v-model="metadata.sample_id" :options="samples" label="Sample" :loading="isLoading"
                                dropdownIcon="search" searchable highlight-matched-text
                                searchPlaceholderText="Type to search" noOptionsText="No sample found">
                            </VaSelect>
                        </div>
                    </div>

                </div>
                <div v-for="(f, index) in fields" :key="index">
                    <h6 class="va-h6">{{ f.title }}</h6>
                    <p class="va-text-secondary mb-2">{{ f.description }}</p>
                    <MetadataForm :existing-metadata="existingMetadata" @update-field="updateModelField"
                        :fields="f.filters">
                    </MetadataForm>
                </div>
            </VaForm>
        </VaInnerLoading>
        <template #footer>
            <div class="row justify-end">
                <div class="flex">
                    <VaButton @click="submit">Submit</VaButton>
                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useForm, useToast } from 'vuestic-ui/web-components';
import { computed, ref } from 'vue';
import MetadataForm from '../forms/MetadataForm.vue'
import ModelID from '../forms/ModelID.vue'
import { ExperimentModel, Filter, SampleModel } from '../../data/types';
import ItemService from '../../services/clients/ItemService';
import { AxiosError } from 'axios';

const props = defineProps<{
    itemToEdit: SampleModel | ExperimentModel | undefined,
}>()

const emits = defineEmits(['itemEdited'])

const schemaStore = useSchemaStore()
const { init } = useToast()
const { validate } = useForm('modelForm')
const samples = ref<string[]>([])

const isLoading = ref(false)
const metadata = ref<Record<string, any>>({})

const existingMetadata = computed(() => {
    if (props.itemToEdit) return Object.entries(props.itemToEdit.metadata)
    return []
})

async function handleSearch(v: string) {
    if (v.length < 2) return
    isLoading.value = true
    try {
        const { data } = await ItemService.getItems(schemaStore.schema.project_id, 'sample', { filter: v })
        samples.value = [...data.data.map((d: SampleModel) => d.sample_id)]
    } catch (error) {
        const axiosError = error as AxiosError
        init({ message: axiosError.message, color: 'danger' })
    } finally {
        isLoading.value = false
    }
}

const idToUpdate = computed(() => {
    if (!props.itemToEdit) return undefined

    let itemID
    if (schemaStore.model === 'experiment') {
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
    for (const f of schemaStore.schema[schemaStore.model].fields) {
        if (schemaStore.schema[schemaStore.model].id_format.includes(f.key) && !idToUpdate.value) {
            idFields.push(f)
        } else if (f.required && !schemaStore.schema[schemaStore.model].id_format.includes(f.key)) {
            requiredFields.push(f)
        } else if (!f.required) {
            optionalFields.push(f)
        }
    }
    const parsedFields = [
        {
            title: 'ID Fields',
            description: 'Provide values for these fields to automatically generate a unique ID.',
            filters: [...idFields]
        },
        {
            title: 'Required Fields',
            description: 'Complete these essential fields to proceed.',
            filters: [...requiredFields]
        },
        {
            title: 'Optional Fields',
            description: 'These fields are optional and can be filled as needed.',
            filters: [...optionalFields]
        },
    ]

    return parsedFields.filter(a => a.filters.length)
})



async function submit() {
    if (!validate()) return
    const allMetadata = { ...Object.fromEntries(existingMetadata.value), ...metadata.value }
    try {

        isLoading.value = true
        if (idToUpdate.value) {
            const response = await ItemService.updateItem(schemaStore.schema.project_id, idToUpdate.value, schemaStore.model, allMetadata as FormData);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `${schemaStore.model} ${idToUpdate.value} edited successfully`,
            });

        } else {
            const response = await ItemService.createItem(schemaStore.schema.project_id, schemaStore.model, allMetadata as FormData);
            const { data } = response;

            init({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `${schemaStore.model} created successfully`,
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
        metadata.value = {}
        emits('itemEdited')
        schemaStore.showForm = false
    }
}

function updateModelField(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {
    metadata.value[tuple[0]] = tuple[1]

}


</script>