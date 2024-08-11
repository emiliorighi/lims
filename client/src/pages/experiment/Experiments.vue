<template>
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardTitle class="va-text-secondary mb-0">Experiment List</VaCardTitle>
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex">
                            <div class="row">
                                <div class="flex">
                                    <TableFilters @on-metadata-update="updateQueryForm"
                                        @on-search-change="updateSearchForm" :columns="columns"
                                        :fields="schemaStore.schema.experiment.fields.filter(f => !singleId || singleId !== f.key)"
                                        @on-show-field-change="updateShowFields" />
                                </div>
                                <div class="flex">
                                    <VaButton :disabled="total === 0" preset="primary"
                                        @click="experimentStore.showReport = !experimentStore.showReport"
                                        icon-right="download">
                                        Report
                                    </VaButton>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <VaButton color="success" icon="add"
                                @click="experimentStore.showForm = !experimentStore.showForm">
                                Experiment
                            </VaButton>
                        </div>
                    </div>
                    <CRUDTable :items="experiments" :columns="columns" @edit-clicked="editExperiment"
                        @delete-clicked="deleteExperiment" />
                    <div class="row align-center justify-space-between">
                        <div class="flex">
                            <b>Total {{ total }}</b>
                            Results per page
                            <VaSelect style="width: 100px;" :options="[10, 20, 50]"
                                v-model="experimentStore.pagination.limit" @update:modelValue="handleLimit" />
                        </div>
                        <div class="flex">
                            <Pagination @offset-changed="handlePagination" :limit="experimentStore.pagination.limit"
                                :offset="experimentStore.pagination.offset" :total="total" />
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
            <ExperimentFormModal @experiment-edited="reset()" />
            <ReportModal :model="'sample'" :search-form="experimentStore.searchForm" :show-modal="experimentStore.showReport" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { computed, onMounted, ref } from 'vue';
import { ExperimentModel, Filter } from '../../data/types';
import ExperimentService from '../../services/clients/ExperimentService';
import { useGlobalStore } from '../../stores/global-store';
import TableFilters from '../../components/filters/TableFilters.vue'
import CRUDTable from '../../components/tables/ItemCRUDTable.vue'
import Pagination from '../../components/filters/Pagination.vue'
import { useExperimentStore } from '../../stores/experiment-store';
import ExperimentFormModal from './components/ExperimentFormModal.vue';
import ReportModal from '../../components/modals/ReportModal.vue'

const schemaStore = useSchemaStore()
const experimentStore = useExperimentStore()
const { toast } = useGlobalStore()

const singleId = computed(() => {
    return schemaStore.schema.sample.id_format.length === 1 ? schemaStore.schema.sample.id_format[0] : undefined
})
const mappedFields = schemaStore.schema.experiment.fields.map((f: Filter) => { return { show: f.required, value: f.key } })

const showFields = ref(mappedFields)

const columns = computed(() => {
    return ['experiment_id', 'sample_id', ...showFields.value.filter(f => f.show).map(f => `metadata.${f.value}`), 'actions']
})

async function updateSearchForm(tuple: ['filter' | 'sort_column' | 'sort_order', Record<string, any>[keyof Record<string, any>]]) {
    const store = { ...experimentStore.searchForm }
    store[tuple[0]] = tuple[1]
    experimentStore.searchForm = { ...store }
    experimentStore.resetPagination()
    await getExperiments()
}


async function updateQueryForm(list: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {
    const { query } = experimentStore.searchForm
    const newQuery = Object.fromEntries(list)
    if (newQuery) {
        experimentStore.searchForm.query = { ...query, ...Object.fromEntries(list) }
    }
    experimentStore.resetPagination()
    await getExperiments()
}

function updateShowFields(updatedShowFields: { show: boolean, value: string }[]) {
    showFields.value = [...updatedShowFields]
}

const experiments = ref<ExperimentModel[]>([])
const total = ref(0)
const errorMessage = ref('')
const isLoading = ref(false)
const offset = ref(1 + experimentStore.pagination.offset)

onMounted(async () => {
    await getExperiments()
})

async function handleLimit(limit: number) {
    experimentStore.pagination.limit = limit
    await getExperiments()
}

async function handlePagination(value: number) {
    experimentStore.pagination.offset = value - 1
    await getExperiments()
}

function editExperiment(index: number) {
    experimentStore.expIdToUpdate = experiments.value[index].sample_id
    experimentStore.showForm = !experimentStore.showForm
}

function parseQuery() {
    let q = { ...experimentStore.pagination }
    const { query, ...fields } = experimentStore.searchForm
    const validFilters = Object.fromEntries(Object.entries(query).filter(([k, v]) => v))
    if (Object.keys(validFilters).length) {
        q = { ...q, ...validFilters }
    }
    if (Object.entries(fields).filter(([k, v]) => v).length) {
        q = { ...q, ...fields }
    }
    return q

}
async function deleteExperiment(index: number) {
    try {
        const expToDelete = experiments.value[index]
        const { data } = await ExperimentService.deleteExperiment(schemaStore.schema.project_id, expToDelete.experiment_id)
        toast({ message: data, color: 'success', duration: 1500 })
    } catch (error) {
        console.error(error)
        toast({ message: 'Error deleting experiment', color: 'danger', duration: 1500 })
    } finally {
        reset()
    }
}

async function reset() {
    offset.value = 1
    experimentStore.resetSeachForm()
    experimentStore.resetPagination()
    await getExperiments()
}

async function getExperiments() {
    const query = parseQuery()
    try {
        const { data } = await ExperimentService.getExperiments(schemaStore.schema.project_id, query)
        experiments.value = [...data.data]
        total.value = data.total
    } catch (e) {
        errorMessage.value = 'Something happened'
    } finally {
        isLoading.value = false
    }
}


</script>
