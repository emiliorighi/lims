<template>
    <Header :title="title" />
    <VaCard>
        <VaCardContent>
            <div class="row justify-space-between">
                <div class="flex">
                    <TableFilters :key="model" @on-metadata-update="updateQueryForm"
                        @on-search-change="updateSearchForm" :columns="columns" :fields="filteredFields"
                        @on-show-field-change="updateShowFields" />
                </div>
                <div class="flex">
                    <div class="row">
                        <div class="flex">
                            <VaButton :disabled="itemStore.total === 0" preset="primary"
                                @click="itemStore.showReport = !itemStore.showReport" icon-right="download">
                                Report
                            </VaButton>
                        </div>
                        <div class="flex">
                            <VaButton icon="add" @click="newItem">
                                {{ buttonLabel }}
                            </VaButton>
                        </div>
                    </div>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <VaDataTable :items="itemStore.items" :columns="columns">
                <template #cell(actions)="{ rowData }">
                    <VaButton v-if="canBeEdited(rowData)" preset="plain" icon="edit" @click="editItem(rowData)" />

                    <VaButton preset="plain" icon="delete" color="danger" class="ml-3"
                        @click="triggerDelete(rowData)" />
                </template>
                <template #cell(sample_id)="{ rowData }">
                    <VaChip @click="showItemDetails(rowData.sample_id, 'sample')" color="textPrimary" flat>
                        {{ rowData.sample_id }}
                    </VaChip>
                </template>
                <template #cell(experiment_id)="{ rowData }">
                    <VaChip v-if="rowData.experiment_id" @click="showItemDetails(rowData.experiment_id, 'experiment')"
                        color="textPrimary" flat>
                        {{ rowData.experiment_id }}
                    </VaChip>
                </template>
            </VaDataTable>
            <Pagination @handle-limit="handleLimit" @offset-changed="handlePagination"
                :limit="itemStore.pagination.limit" :offset="itemStore.pagination.offset" :total="itemStore.total" />
        </VaCardContent>
    </VaCard>
    <ReportModal :model="model" :icon="icon" />

    <ConfirmDeleteModal :model="model" :icon="icon" />

    <ModelFormModal :model="model" :icon="icon" />

    <ItemDetailsModal :icon="icon" />

</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useSchemaStore } from '../../../stores/schemas-store'
import TableFilters from '../../../components/filters/TableFilters.vue'
import ReportModal from '../../../components/modals/ReportModal.vue'
import ModelFormModal from '../../../components/modals/ModelFormModal.vue'
import ItemDetailsModal from '../../../components/modals/ItemDetailsModal.vue'
import { ItemModel, ModelType } from '../../../data/types';
import Pagination from '../../../components/filters/Pagination.vue'
import { useItemStore } from '../../../stores/item-store'
import ConfirmDeleteModal from '../../../components/modals/ConfirmDeleteModal.vue'
import Header from '../../../components/ui/Header.vue'

const itemStore = useItemStore()

const schemaStore = useSchemaStore()
const { project_id } = schemaStore.schema

const props = defineProps<{
    model: ModelType,
    title: string,
    buttonLabel: string,
    icon: string
}>()

onMounted(async () => {
    await itemStore.fetchItems(schemaStore.schema.project_id, props.model)
})
watch(() => props.model, async (v) => {
    itemStore.resetPagination()
    itemStore.resetSearchForm()
    await itemStore.fetchItems(project_id, v)
})

const singleId = computed(() =>
    schemaStore.schema[props.model].id_format.length === 1
        ? schemaStore.schema[props.model].id_format[0]
        : undefined
);

const idColumns = computed(() => {
    return props.model === 'experiment' ? ['experiment_id', 'sample_id'] : ['sample_id'];
})
const filteredFields = computed(() =>
    schemaStore.schema[props.model].fields.filter(f => !singleId.value || singleId.value !== f.key)
);

const showFields = ref(
    schemaStore.schema[props.model].fields.map(f => ({ show: f.required, value: f.key }))
);

const columns = computed(() => {
    return [...idColumns.value, ...showFields.value.filter(f => f.show).map(f => `metadata.${f.value}`), 'actions'];
});

async function updateSearchForm(tuple: ['filter' | 'sort_column' | 'sort_order', Record<string, any>[keyof Record<string, any>]]) {
    const { searchForm } = itemStore
    searchForm[tuple[0]] = tuple[1]
    itemStore.searchForm = { ...searchForm }
    itemStore.resetPagination()
    itemStore.fetchItems(project_id, props.model)
}

async function updateQueryForm(list: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {
    const { query } = itemStore.searchForm
    const newQuery = Object.fromEntries(list)
    if (newQuery) {
        itemStore.searchForm.query = { ...query, ...Object.fromEntries(list) }
    }
    itemStore.resetPagination()
    await itemStore.fetchItems(project_id, props.model)
}


function updateShowFields(updatedShowFields: { show: boolean, value: string }[]) {
    showFields.value = [...updatedShowFields]
}

async function showItemDetails(id: string, model: ModelType) {
    await itemStore.fetchItem(project_id, id, model)
}

function triggerDelete(rowData: ItemModel) {
    itemStore.idToDelete = rowData.experiment_id ? rowData.experiment_id : rowData.sample_id
    itemStore.showDeleteConfirm = !itemStore.showDeleteConfirm
}

function canBeEdited(rowData: ItemModel) {
    const { id_format, fields } = schemaStore.schema[props.model]
    const optionalFields = fields.filter(f => !f.required)
    return id_format.length !== Object.keys(rowData.metadata).length || optionalFields.length
}

async function handleLimit(limit: number) {
    itemStore.pagination.limit = limit;
    await itemStore.fetchItems(project_id, props.model)
}

async function handlePagination(offset: number) {
    itemStore.pagination.offset = offset - 1;
    await itemStore.fetchItems(project_id, props.model)
}


function editItem(rowData: ItemModel) {
    itemStore.item = { ...rowData }
    itemStore.showForm = !itemStore.showForm;
}

function newItem() {
    itemStore.item = undefined
    itemStore.showForm = !itemStore.showForm;
}

async function reset() {
    itemStore.resetPagination()
    itemStore.resetSearchForm()
    await itemStore.fetchItems(project_id, props.model)
}


</script>