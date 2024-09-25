<template>
    <VaDataTable @columnSorted="sortItems" disableClientSideSorting @row:click="showItemDetails" hoverable clickable
        :loading="isLoading" :items="items" :columns="columns">
        <template v-if="isAuthorized" #cell(actions)="{ rowData }">
            <VaButton v-if="canBeEdited" preset="plain" icon="edit" @click.stop.prevent="editItem(rowData)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3"
                @click.stop.prevent="triggerDelete(rowData)" />
        </template>
    </VaDataTable>
    <ModelFormModal :model="model" :icon="icon" />
    <ConfirmDeleteModal @confirmDelete="deleteItem" :idToDelete="idToDelete" :icon="icon" />
    <ItemDetailsModal :icon="icon" />
    <ReportModal :model="model" :icon="icon" />

</template>

<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store'
import { Filter } from '../../data/types'
import { computed, ref } from 'vue';
import { useGlobalStore } from '../../stores/global-store'
import { useItemStore } from '../../stores/item-store';
import ModelFormModal from '../modals/ModelFormModal.vue';
import ConfirmDeleteModal from '../modals/ConfirmDeleteModal.vue';
import ItemDetailsModal from '../modals/ItemDetailsModal.vue';
import ReportModal from '../modals/ReportModal.vue';

const itemStore = useItemStore()
const schemaStore = useSchemaStore()
const globalStore = useGlobalStore()
const isLoading = ref(false)
const idToDelete = ref('')
const props = defineProps<{
    items: Record<string, any>[],
    filters: Filter[],
    projectId: string,
    isAuthorized: boolean
}>();

const model = computed(() => itemStore.currentModel)
const icon = computed(() => model.value === 'experiment' ? 'fa-dna' : 'fa-vial')
const idColumns = computed(() => {
    const sample = { label: 'Sample id', key: 'sample_id', sortable: true }
    return itemStore.currentModel === 'experiment'
        ? [{ label: 'Experiment id', key: 'experiment_id', sortable: true }, sample]
        : [sample];
})

const columns = computed(() => {
    const cols = props.filters.map(({ key, label }) => { return { sortable: true, key, label } })
    if (globalStore.isAuthenticated) cols.push({ key: 'actions', label: 'actions', sortable: false })
    return [...idColumns.value, ...cols]
})

function editItem(rowData: any) {
    itemStore.stores[model.value].item = { ...rowData }
    itemStore.showForm = !itemStore.showForm
}

function triggerDelete(rowData: any) {
    idToDelete.value = rowData.experiment_id ? rowData.experiment_id : rowData.sample_id
    globalStore.showDeleteConfirmation = !globalStore.showDeleteConfirmation
}

async function deleteItem() {
    await itemStore.deleteItem(props.projectId, idToDelete.value)
    itemStore.resetPagination()
    itemStore.resetSearchForm()
    await itemStore.fetchItems(props.projectId)
    globalStore.showDeleteConfirmation = !globalStore.showDeleteConfirmation
}

async function showItemDetails(payload: any) {
    const { row } = payload
    let id = row.rowData.sample_id
    if (model.value === 'experiment') id = row.rowData.experiment_id
    await itemStore.fetchItem(props.projectId, id)
}

const canBeEdited = computed(() => {
    const idFormat = schemaStore.schema[model.value].id_format;
    const fields = schemaStore.schema[model.value].fields;
    const optionalFields = fields.filter(f => !f.required);

    return idFormat.length !== fields.length || optionalFields.length;
})

async function sortItems(event: { columnName: string, value: 'asc' | 'desc' | null, column: any },) {
    const { columnName, value } = event
    itemStore.stores[model.value].sort.sort_column = columnName
    itemStore.stores[model.value].sort.sort_order = value
    await itemStore.fetchItems(props.projectId)
}
</script>
