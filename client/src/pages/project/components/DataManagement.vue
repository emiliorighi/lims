<template>
    <div>
        <h4 class="va-h4">{{ title }}</h4>
        <p class="va-text-secondary mb-4">{{ description }}</p>

        <div class="row justify-space-between">
            <div class="flex">
                <TableFilters @on-metadata-update="updateQueryForm" @on-search-change="updateSearchForm"
                    :columns="columns" :fields="filteredFields" @on-show-field-change="updateShowFields" />
            </div>
            <div class="flex">
                <div class="row">
                    <div class="flex">
                        <VaButton :disabled="total === 0" preset="primary" @click="showReport" icon-right="download">
                            Report
                        </VaButton>
                    </div>
                    <div class="flex">
                        <VaButton icon="add" @click="showForm">
                            {{ addButtonLabel }}
                        </VaButton>
                    </div>
                </div>
            </div>
        </div>
        <CRUDTable :items="items" :columns="columns" @show-sample-details="showSampleDetails"
            @show-experiment-details="showExperimentDetails" @edit-clicked="editItem" @delete-clicked="deleteItem" />

        <Pagination @handle-limit="handleLimit" @offset-changed="handlePagination" :limit="pagination.limit"
            :offset="pagination.offset" :total="total" />



        <ModelFormModal @item-edited="reset" :item-to-edit="itemToEdit" />

        <ReportModal :search-form="itemStore().searchForm" />

        <ItemDetailsModal v-if="item" :id="itemID" :icon="itemIcon" :metadata="item.metadata" />

    </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { useGlobalStore } from '../../../stores/global-store';
import { useSchemaStore } from '../../../stores/schemas-store'
import TableFilters from '../../../components/filters/TableFilters.vue'
import CRUDTable from '../../../components/tables/ItemCRUDTable.vue'
import ReportModal from '../../../components/modals/ReportModal.vue'
import ModelFormModal from '../../../components/modals/ModelFormModal.vue'
import ItemDetailsModal from '../../../components/modals/ItemDetailsModal.vue'
import { SampleModel, ExperimentModel, ModelType } from '../../../data/types';
import Pagination from '../../../components/filters/Pagination.vue'
import ItemService from '../../../services/clients/ItemService'
import { useSampleStore } from '../../../stores/sample-store'
import { useExperimentStore } from '../../../stores/experiment-store'
import { AxiosError } from 'axios'


const schemaStore = useSchemaStore()
// Props
const { model } = schemaStore
const props = defineProps<{
    itemStore: typeof useSampleStore | typeof useExperimentStore,
    addButtonLabel: string,
    title: string
    description: string
}>();

const store = props.itemStore()
const { toast } = useGlobalStore();

const items = ref<SampleModel[] | ExperimentModel[]>([]);
const item = ref<SampleModel | ExperimentModel>()
const itemID = ref('')
const itemIcon = ref<'fa-vial' | 'fa-dna'>('fa-vial')
const total = ref(0);
const itemToEdit = ref<SampleModel | ExperimentModel | undefined>()
const errorMessage = ref('');
const pagination = ref({ limit: 10, offset: 0 });
const singleId = computed(() => {
    return schemaStore.schema[model].id_format.length === 1
        ? schemaStore.schema[model].id_format[0]
        : undefined;
});
const filteredFields = computed(() => {
    return schemaStore.schema[model].fields.filter(f => !singleId.value || singleId.value !== f.key);
});

const showFields = ref(schemaStore.schema[model].fields.map(f => {
    return { show: f.required, value: f.key };
}));

const columns = computed(() => {
    const ids = []
    if (model === 'experiment') {
        ids.push('experiment_id')
    }
    ids.push('sample_id')
    return [...ids, ...showFields.value.filter(f => f.show).map(f => `metadata.${f.value}`), 'actions'];
});

async function updateSearchForm(tuple: ['filter' | 'sort_column' | 'sort_order', Record<string, any>[keyof Record<string, any>]]) {
    const searchForm = { ...store.searchForm }
    searchForm[tuple[0]] = tuple[1]
    store.searchForm = { ...searchForm }
    store.resetPagination()
    await fetchItems()
}

async function updateQueryForm(list: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {
    const { query } = store.searchForm
    const newQuery = Object.fromEntries(list)
    if (newQuery) {
        store.searchForm.query = { ...query, ...Object.fromEntries(list) }
    }
    store.resetPagination()
    await fetchItems()
}


function updateShowFields(updatedShowFields: { show: boolean, value: string }[]) {
    showFields.value = [...updatedShowFields]
}

async function showSampleDetails(id: string) {
    itemID.value = id
    itemIcon.value = 'fa-vial'
    await fetchItem(schemaStore.schema.project_id, id, 'sample')
}

async function showExperimentDetails(id: string) {
    itemID.value = id
    itemIcon.value = 'fa-dna'
    await fetchItem(schemaStore.schema.project_id, id, 'experiment')
}
async function handleLimit(limit: number) {
    store.pagination.limit = limit;
    await fetchItems();
}

async function handlePagination(offset: number) {
    store.pagination.offset = offset - 1;
    await fetchItems();
}

function editItem(index: number) {
    itemToEdit.value = items.value[index];
    schemaStore.showForm = !schemaStore.showForm;
}

function parseQuery() {
    let q = { ...store.pagination }
    const { query, ...fields } = store.searchForm
    const validFilters = Object.fromEntries(Object.entries(query).filter(([k, v]) => v))
    if (Object.keys(validFilters).length) {
        q = { ...q, ...validFilters }
    }
    if (Object.entries(fields).filter(([k, v]) => v).length) {
        q = { ...q, ...fields }
    }
    return q

}
async function deleteItem(index: number) {
    try {
        const itemToDelete = items.value[index];
        let id

        if ('experiment_id' in itemToDelete) {
            id = itemToDelete.experiment_id
        } else {
            id = itemToDelete.sample_id
        }
        const { data } = await ItemService.deleteItem(schemaStore.schema.project_id, id, model);
        toast({ message: data, color: 'success', duration: 1500 });
        reset();
    } catch (error) {
        console.error(error);
        toast({ message: 'Error deleting item', color: 'danger', duration: 1500 });
    }
}

function showReport() {
    schemaStore.showReport = !schemaStore.showReport;
}

function showForm() {
    itemToEdit.value = undefined;
    schemaStore.showForm = !schemaStore.showForm;
}

async function reset() {
    pagination.value.offset = 0;
    store.searchForm.query = {};
    await fetchItems();
}

async function fetchItems() {
    const query = parseQuery();
    try {
        const { data } = await ItemService.getItems(schemaStore.schema.project_id, model, query);
        items.value = [...data.data];
        total.value = data.total;
    } catch (e) {
        errorMessage.value = 'Something went wrong';
    }
}
async function fetchItem(projectId: string, itemId: string, m: ModelType) {
    try {
        const { data } = await ItemService.getItem(projectId, itemId, m)
        item.value = { ...data }
        schemaStore.showDetails = true
    } catch (e) {
        let message: string
        const axiosError = e as AxiosError

        if (axiosError.response?.data) {
            message = (axiosError.response.data as { message: string }).message || axiosError.response.data as string
        } else {
            message = axiosError.message
        }

        toast({ message: message, color: 'danger' })
    }

}
onMounted(async () => {
    await fetchItems();
});
</script>