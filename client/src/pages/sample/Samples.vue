<template>
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardTitle class="va-text-secondary mb-0">Sample List</VaCardTitle>
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex">
                            <div class="row">
                                <div class="flex">
                                    <TableFilters @on-metadata-update="updateQueryForm"
                                        @on-search-change="updateSearchForm" :columns="columns"
                                        :fields="schemaStore.schema.sample.fields.filter(f => !singleId || singleId !== f.key)"
                                        @on-show-field-change="updateShowFields" />
                                </div>
                                <div class="flex">
                                    <VaButton :disabled="total === 0" preset="primary"
                                        @click="sampleStore.showReport = !sampleStore.showReport" icon-right="download">
                                        Report
                                    </VaButton>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <VaButton icon="add" @click="sampleStore.showForm = !sampleStore.showForm">
                                Sample
                            </VaButton>
                        </div>
                    </div>
                    <CRUDTable :items="samples" :columns="columns" @edit-clicked="editSample"
                        @delete-clicked="deleteSample" />
                    <div class="row align-center justify-space-between">
                        <div class="flex">
                            <b>Total {{ total }}</b>
                            Results per page
                            <VaSelect style="width: 100px;" :options="[10, 20, 50]"
                                v-model="sampleStore.pagination.limit" />
                        </div>
                        <div class="flex">
                            <Pagination @offset-changed="handlePagination" :limit="sampleStore.pagination.limit"
                                :offset="sampleStore.pagination.offset" :total="total" />
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
            <SampleFormModal @sample-edited="handleSubmit" />
            <ReportModal />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSampleStore } from '../../stores/sample-store';
import { useSchemaStore } from '../../stores/schemas-store';
import { computed, onMounted, ref } from 'vue';
import { Filter, SampleModel } from '../../data/types';
import SampleService from '../../services/clients/SampleService';
import { useGlobalStore } from '../../stores/global-store';
import TableFilters from '../../components/filters/TableFilters.vue'
import CRUDTable from '../../components/data/ItemCRUDTable.vue'
import Pagination from '../../components/filters/Pagination.vue'
import SampleFormModal from './components/SampleFormModal.vue';
import ReportModal from './components/ReportModal.vue'


const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { toast } = useGlobalStore()

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
    await handleSubmit()
}

async function updateQueryForm(list: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {

    //check ranges
    const { query } = sampleStore.searchForm
    const newQuery = { query: { ...query, ...Object.fromEntries(list) } }
    sampleStore.searchForm = { ...sampleStore.searchForm, ...newQuery }
    handleSubmit()
}

function updateShowFields(updatedShowFields: { show: boolean, value: string }[]) {
    showFields.value = [...updatedShowFields]
}

const samples = ref<SampleModel[]>([])
const total = ref(0)
const isLoading = ref(false)
const offset = ref(1 + sampleStore.pagination.offset)

onMounted(async () => {
    await handleSubmit()
})

async function handleSubmit() {
    sampleStore.resetPagination()
    offset.value = 1
    const { query, ...fields } = sampleStore.searchForm
    await getSamples({ ...query, ...fields, ...sampleStore.pagination })
}

async function handlePagination(value: number) {
    sampleStore.pagination.offset = value - 1
    await getSamples({ ...sampleStore.searchForm, ...sampleStore.pagination })
}

function editSample(index: number) {
    sampleStore.sampleIdToUpdate = samples.value[index].sample_id
    sampleStore.showForm = !sampleStore.showForm
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
    sampleStore.resetPagination()
    await handleSubmit()
}


async function getSamples(query: Record<string, any>) {
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
