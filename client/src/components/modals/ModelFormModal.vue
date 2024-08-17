<template>
    <VaModal hide-default-actions max-height="500px" fixed-layout v-model="itemStore.showForm">
        <template #header>
            <Header :title="idToUpdate ? `Update ${idToUpdate}` : `Create ${model}`" :icon="icon" />
        </template>
        <VaDivider />
        <VaInnerLoading :loading="itemStore.isLoading">
            <VaForm ref="modelForm">
                <div v-if="!idToUpdate">
                    <ItemID :id="id" :rules="rules" />
                    <SampleLinking v-if="model === 'experiment'" :model="props.model" :metadata="metadata.value"
                        :samples="samples" :selectLoading="selectLoading" @update:search="handleSearch" />
                </div>
                <div v-for="(f, index) in fields" :key="index">
                    <h6 class="va-h6">{{ f.title }}</h6>
                    <p class="va-text-secondary mb-2">{{ f.description }}</p>
                    <MetadataForm :existing-metadata="existingMetadata"
                        @update-field="(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) => metadata.value[tuple[0]] = tuple[1]"
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
import { AxiosError } from 'axios';
import { computed, reactive, ref, watch } from 'vue';

import { useSchemaStore } from './../../stores/schemas-store';
import { useToast, useForm } from 'vuestic-ui/web-components';
import { useItemStore } from '../../stores/item-store'

import { ItemModel, Filter, ModelType } from '../../data/types';

import ItemService from '../../services/clients/ItemService';

import Header from './common/Header.vue'

import MetadataForm from '../forms/MetadataForm.vue'
import SampleLinking from '../forms/SampleLinking.vue'
import ItemID from '../forms/ItemID.vue'

const props = defineProps<{
    model: ModelType
    icon: string

}>()

const { init } = useToast()
const itemStore = useItemStore()
const schemaStore = useSchemaStore()
const { validate } = useForm('modelForm')

const modelExists = ref(false)
const samples = ref<string[]>([])
const selectLoading = ref(false)
const idGeneratorLoading = ref(false)
const metadata = reactive<Record<string, any>>({ value: {} })

// Computed Properties
const existingMetadata = computed(() => {
    return itemStore.item ? Object.entries(itemStore.item.metadata) : [];
});

const id = computed(() => {
    // Track all keys in metadata by converting it to a string
    const metadataString = JSON.stringify(metadata.value);
    const keys = schemaStore.schema[props.model].id_format;
    const idFields = Object.entries(metadata.value).filter(([k, v]) => keys.includes(k) && v);
    if (keys.length > idFields.length) return ' ';
    return idFields.map(([k, v]) => v).join('_');
});

const rules = computed(() => {
    return [(v: string) => v.length > 0 || 'Fill the required fields to generate the unique identifier',
    !modelExists.value || `${props.model} already exists`]
})

const idToUpdate = computed(() => {
    if (!itemStore.item) return undefined
    return itemStore.item.experiment_id ? itemStore.item.experiment_id : itemStore.item.sample_id
})

const fields = computed(() => {
    const { id_format, fields } = schemaStore.schema[props.model];
    const idFields = fields.filter(f => id_format.includes(f.key) && !idToUpdate.value);
    const requiredFields = fields.filter(f => f.required && !id_format.includes(f.key));
    const optionalFields = fields.filter(f => !f.required);

    return [
        createFieldGroup('ID Fields', 'Provide values for these fields to automatically generate a unique ID.', idFields),
        createFieldGroup('Required Fields', 'Complete these essential fields to proceed.', requiredFields),
        createFieldGroup('Optional Fields', 'These fields are optional and can be filled as needed.', optionalFields),
    ].filter(group => group.filters.length);
});
// Watchers
watch(() => (id.value), async () => {
    if (!id.value) return
    await getItem(id.value)
})
// Methods
function createFieldGroup(title: string, description: string, filters: Filter[]) {
    return { title, description, filters };
}

async function handleSearch(query: string) {
    if (query.length < 2) return;
    selectLoading.value = true;

    try {
        const { data } = await ItemService.getItems(schemaStore.schema.project_id, 'sample', { filter: query });
        samples.value = data.data.map((d: ItemModel) => d.sample_id);
    } catch (error) {
        handleError(error, 'Error fetching samples');
    } finally {
        selectLoading.value = false;
    }
}

async function getItem(id: string) {
    try {
        idGeneratorLoading.value = true;
        const { data } = await ItemService.getItem(schemaStore.schema.project_id, id, props.model);
        modelExists.value = !!data;
        if (data) {
            init({ message: `${props.model} with ${id} already exists`, color: 'danger' });
        }
    } catch (error) {
        if (error instanceof AxiosError && error.response?.status === 404) {
            modelExists.value = false;
        } else {
            handleError(error, 'Error fetching item');
        }
    } finally {
        idGeneratorLoading.value = false;
    }
}
async function submit() {
    if (!validate()) return;
    itemStore.isLoading = true;

    const allMetadata = { ...Object.fromEntries(existingMetadata.value), ...metadata.value };

    try {
        const response = idToUpdate.value
            ? await ItemService.updateItem(schemaStore.schema.project_id, idToUpdate.value, props.model, allMetadata as FormData)
            : await ItemService.createItem(schemaStore.schema.project_id, props.model, allMetadata as FormData);

        itemStore.toast({
            color: 'success',
            message: Array.isArray(response.data)
                ? response.data.join(', ')
                : `${props.model} ${idToUpdate.value ? `${idToUpdate.value} edited` : 'created'} successfully`,
        });

        resetForm();
    } catch (error) {
        handleError(error, 'Error saving item');
    } finally {
        itemStore.isLoading = false;
    }
}

function handleError(error: any, defaultMessage: string) {
    console.error(defaultMessage, error);
    const message = error instanceof AxiosError ? error.response?.data?.message || defaultMessage : defaultMessage;
    itemStore.toast({ color: 'danger', message });
}

function resetForm() {
    metadata.value = {};
    itemStore.resetSearchForm();
    itemStore.resetPagination();
    itemStore.fetchItems(schemaStore.schema.project_id, props.model);
    itemStore.showForm = false;
}
</script>