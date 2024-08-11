<template>
    <div class="row justify-space-between align-end">
        <h1 class="va-h1 flex pt-0">Samples </h1>
        <div class="flex">
            <VaButton color="success" icon="add" @click="sampleStore.showForm = !sampleStore.showForm">
                Sample
            </VaButton>
        </div>
    </div>
    <VaCard>
        <VaCardContent class="row">
            <div class="flex">
                <TableFilters @on-metadata-update="updateQueryForm" @on-search-change="updateSearchForm"
                    :columns="columns"
                    :fields="schemaStore.schema.sample.fields.filter(f => !singleId || singleId !== f.key)"
                    @on-show-field-change="updateShowFields" />
            </div>
            <div class="flex">
                <VaButton :disabled="total === 0" preset="primary"
                    @click="sampleStore.showReport = !sampleStore.showReport" icon-right="download">
                    Report
                </VaButton>
            </div>
            <CRUDTable :items="samples" :columns="columns" @edit-clicked="editSample" @delete-clicked="deleteSample" />
            <div class="row align-center justify-space-between">
                <div class="flex">
                    <b>Total {{ total }}</b>
                    Results per page
                    <VaSelect style="width: 100px;" :options="[10, 20, 50]" v-model="sampleStore.pagination.limit" />
                </div>
                <div class="flex">
                    <Pagination @offset-changed="handlePagination" :limit="sampleStore.pagination.limit"
                        :offset="sampleStore.pagination.offset" :total="total" />
                </div>
            </div>
        </VaCardContent>
    </VaCard>
    <ReportModal @on-close="sampleStore.showReport = !sampleStore.showReport" :model="'sample'"
        :search-form="sampleStore.searchForm" :show-modal="sampleStore.showReport" />
    <ModelFormModal @on-cancel="reset" :show-form="sampleStore.showForm" :model="'sample'" :item-to-edit="itemToEdit" />
</template>

<script setup lang="ts">
import { useSampleStore } from '../../stores/sample-store';
import { useSchemaStore } from '../../stores/schemas-store';
import { computed, onMounted, ref } from 'vue';
import { Filter, SampleModel } from '../../data/types';
import SampleService from '../../services/clients/SampleService';
import { useGlobalStore } from '../../stores/global-store';
import TableFilters from '../../components/filters/TableFilters.vue'
import CRUDTable from '../../components/tables/ItemCRUDTable.vue'
import Pagination from '../../components/filters/Pagination.vue'
import ReportModal from '../../components/modals/ReportModal.vue'
import ModelFormModal from '../../components/modals/ModelFormModal.vue'


const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { toast } = useGlobalStore()

const itemToEdit = ref<SampleModel | undefined>()

const singleId = computed(() => {
    return schemaStore.schema.sample.id_format.length === 1 ? schemaStore.schema.sample.id_format[0] : undefined
})
const mappedFields = ref(schemaStore.schema.sample.fields.filter(f => !singleId.value || singleId.value !== f.key).map((f: Filter) => { return { show: f.required, value: f.key } }))

const showFields = ref([...mappedFields.value])

const columns = computed(() => {

    return ['sample_id', ...showFields.value.filter(f => f.show).filter(f => !singleId.value || singleId.value !== f.value).map(f => `metadata.${f.value}`), 'actions']
})

async function updateSearchForm(tuple: ['filter' | 'sort_column' | 'sort_order', Record<string, any>[keyof Record<string, any>]]) {
    const store = { ...sampleStore.searchForm }
    store[tuple[0]] = tuple[1]
    sampleStore.searchForm = { ...store }
    await getSamples()
}

async function updateQueryForm(list: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {

    //check ranges
    const { query } = sampleStore.searchForm
    const newQuery = { query: { ...query, ...Object.fromEntries(list) } }
    sampleStore.searchForm = { ...sampleStore.searchForm, ...newQuery }
    getSamples()
}

function updateShowFields(updatedShowFields: { show: boolean, value: string }[]) {
    showFields.value = [...updatedShowFields]
}

const samples = ref<SampleModel[]>([])
const total = ref(0)
const isLoading = ref(false)
const offset = ref(1 + sampleStore.pagination.offset)

onMounted(async () => {
    await getSamples()
})


async function handlePagination(value: number) {
    sampleStore.pagination.offset = value - 1
    await getSamples()
}

function editSample(index: number) {
    itemToEdit.value = samples.value[index]
    // sampleStore.sampleIdToUpdate = samples.value[index].sample_id
    sampleStore.showForm = !sampleStore.showForm
}

function parseQuery() {
    let q = { ...sampleStore.pagination }
    const { query, ...fields } = sampleStore.searchForm
    const validFilters = Object.fromEntries(Object.entries(query).filter(([k, v]) => v))
    if (Object.keys(validFilters).length) {
        q = { ...q, ...validFilters }
    }
    if (Object.entries(fields).filter(([k, v]) => v).length) {
        q = { ...q, ...fields }
    }
    return q

}

async function deleteSample(index: number) {
    try {
        const sampleToDelete = samples.value[index]
        const { data } = await SampleService.deleteSample(schemaStore.schema.project_id, sampleToDelete.sample_id)
        toast({ message: data, color: 'success', duration: 1500 })
    } catch (error) {
        console.error(error)
        toast({ message: 'Error deleting sample', color: 'danger', duration: 1500 })
    } finally {
        reset()
    }
}

async function reset() {
    offset.value = 1
    sampleStore.resetSeachForm()
    sampleStore.showForm = false
    sampleStore.resetPagination()
    await getSamples()
}


async function getSamples() {
    const query = parseQuery()
    try {
        const { data } = await SampleService.getSamples(schemaStore.schema.project_id, query)
        samples.value = [...data.data]
        total.value = data.total
    } catch (e) {
        console.error(e)
    } finally {
        isLoading.value = false
    }
}

</script>
