<template>
    <VaModal hide-default-actions max-height="500px" fixed-layout v-model="itemStore.showForm">

        <template #header>
            <div class="row align-center justify-space-between">
                <h3 class=" flex va-h3">
                    {{ idToUpdate ? `Update ${idToUpdate}` : `Create ${model}` }}
                </h3>
                <VaIcon color="primary" size="large" class="flex" :name="icon" />
            </div>
        </template>
        <VaDivider />
        <VaInnerLoading :loading="itemStore.isLoading">
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
                                v-model="metadata.sample_id" :options="samples" label="Sample" :loading="selectLoading"
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
import { useForm } from 'vuestic-ui/web-components';
import { computed, ref } from 'vue';
import MetadataForm from '../forms/MetadataForm.vue'
import ModelID from '../forms/ModelID.vue'
import { ItemModel, Filter, ModelType } from '../../data/types';
import ItemService from '../../services/clients/ItemService';
import { AxiosError } from 'axios';
import { useItemStore } from '../../stores/item-store'

const itemStore = useItemStore()
const schemaStore = useSchemaStore()
const { validate } = useForm('modelForm')
const samples = ref<string[]>([])
const selectLoading = ref(false)
const props = defineProps<{
    model: ModelType
    icon: string

}>()
const metadata = ref<Record<string, any>>({})

const existingMetadata = computed(() => {
    if (itemStore.item) return Object.entries(itemStore.item.metadata)
    return []
})

async function handleSearch(v: string) {
    if (v.length < 2) return
    selectLoading.value = true
    try {
        const { data } = await ItemService.getItems(schemaStore.schema.project_id, 'sample', { filter: v })
        samples.value = [...data.data.map((d: ItemModel) => d.sample_id)]
    } catch (error) {
        const axiosError = error as AxiosError
        itemStore.toast({ message: axiosError.message, color: 'danger' })
    } finally {
        selectLoading.value = false
    }
}

const idToUpdate = computed(() => {
    if (!itemStore.item) return undefined

    return itemStore.item.experiment_id ? itemStore.item.experiment_id : itemStore.item.sample_id

})

const fields = computed(() => {

    const requiredFields = [] as Filter[]
    const optionalFields = [] as Filter[]
    const idFields = [] as Filter[]
    for (const f of schemaStore.schema[props.model].fields) {
        if (schemaStore.schema[props.model].id_format.includes(f.key) && !idToUpdate.value) {
            idFields.push(f)
        } else if (f.required && !schemaStore.schema[props.model].id_format.includes(f.key)) {
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

        itemStore.isLoading = true
        if (idToUpdate.value) {
            const response = await ItemService.updateItem(schemaStore.schema.project_id, idToUpdate.value, schemaStore.model, allMetadata as FormData);
            const { data } = response;

            itemStore.toast({
                color: 'success',
                message: Array.isArray(data) ? data.join(', ') : `${schemaStore.model} ${idToUpdate.value} edited successfully`,
            });

        } else {
            const response = await ItemService.createItem(schemaStore.schema.project_id, schemaStore.model, allMetadata as FormData);
            const { data } = response;

            itemStore.toast({
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
        itemStore.toast({
            color: 'danger',
            message,
        });
    } finally {
        itemStore.isLoading = false
        metadata.value = {}
        itemStore.resetPagination()
        itemStore.resetSearchForm()
        await itemStore.fetchItems(schemaStore.schema.project_id, props.model)
        itemStore.showForm = false
    }
}

function updateModelField(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {
    metadata.value[tuple[0]] = tuple[1]

}


</script>