<template>
    <Header :title="title" />
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
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
                    <ItemsTable :items="itemStore.items" :columns="columns" :model="model" @edit-item="editItem"
                        @trigger-delete="triggerDelete" @show-item-details="showItemDetails" />
                    <Pagination @handle-limit="handleLimit" @offset-changed="handlePagination"
                        :limit="itemStore.pagination.limit" :offset="itemStore.pagination.offset"
                        :total="itemStore.total" />
                </VaCardContent>
            </VaCard>
        </div>
    </div>

    <ReportModal :model="model" :icon="icon" />

    <ConfirmDeleteModal :model="model" :icon="icon" />

    <ModelFormModal :model="model" :icon="icon" />

    <ItemDetailsModal :icon="itemType === 'sample' ? 'fa-vial' : 'fa-dna'" />

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
import ItemsTable from '../../../components/tables/ItemsTable.vue'

const itemStore = useItemStore()
const schemaStore = useSchemaStore()
const { project_id } = schemaStore.schema

const props = defineProps<{
    model: ModelType,
    title: string,
    buttonLabel: string,
    icon: string
}>()

const itemType = ref<ModelType>('sample')
const showFields = ref(
    schemaStore.schema[props.model].fields.map(f => ({ show: f.required, value: f.key }))
)

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
)
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

async function showItemDetails(payload: { id: string, model: ModelType }) {
    const { id, model } = payload
    itemType.value = model
    await itemStore.fetchItem(project_id, id, model)
}

function triggerDelete(rowData: ItemModel) {
    itemStore.idToDelete = rowData.experiment_id ? rowData.experiment_id : rowData.sample_id
    itemStore.showDeleteConfirm = !itemStore.showDeleteConfirm
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


</script>