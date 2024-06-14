<template>
    <div>
        <h1 class="va-h1">List of Samples</h1>
        <p style="margin-bottom: 6px" class="va-text-secondary"></p>
        <div class="row row-equal">
            <div class="flex lg12 md12 sm12 xs12">
                <VaCard>
                    <VaCardContent class="row justify-space-between">
                        <div class="flex">
                            <TableFilters :columns="columns" :fields="schemaStore.schema.sample.fields"
                                @on-filter-change="updateSearchForm" @on-show-field-change="updateShowFields" />
                        </div>
                        <div class="flex">
                            <SampleListActions />
                        </div>
                    </VaCardContent>
                    <VaCardContent>
                        <CRUDTable :items="samples" :columns="columns" @edit-clicked="editSample"
                            @delete-clicked="deleteSample" />
                    </VaCardContent>
                    <VaDivider />
                    <VaCardContent class="row justify-center">
                        <div class="flex">
                            <Pagination @offset-changed="handlePagination" :limit="sampleStore.pagination.limit"
                                :off-set="sampleStore.pagination.offset" :total="total" />
                        </div>
                    </VaCardContent>
                </VaCard>
            </div>
            <SampleFormModal @on-sample-edited="reset" v-if="schemaStore.schema.project_id" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSampleStore } from '../../stores/sample-store';
import { useSchemaStore } from '../../stores/schemas-store';
// import SampleForm from './SampleForm.vue';
import { computed, onMounted, ref } from 'vue';
import { Filter, SampleModel, ModelSearchForm } from '../../data/types';
import SampleService from '../../services/clients/SampleService';
import { useGlobalStore } from '../../stores/global-store';
import TableFilters from '../../components/filters/TableFilters.vue'
import CRUDTable from '../../components/data/ItemCRUDTable.vue'
import Pagination from '../../components/filters/Pagination.vue'
import TsvImport from '../../components/forms/TsvImport.vue';
import DragAndDrop from '../../components/forms/DragAndDrop.vue';
import ProjectService from '../../services/clients/ProjectService';
import SampleListActions from './components/SampleListActions.vue';
import SampleFormModal from './components/SampleFormModal.vue';

const props = defineProps<{
    projectId: string
}>()

const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { toast } = useGlobalStore()


const mappedFields = schemaStore.schema.sample.fields.map((f: Filter) => { return { show: f.required, value: f.key } })

const showFields = ref(mappedFields)

const columns = computed(() => {
    return ['sample_id', ...showFields.value.filter(f => f.show).map(f => `metadata.${f.value}`), 'actions']
})

function updateSearchForm(payload: ModelSearchForm) {
    sampleStore.searchForm = { ...payload }
    handleSubmit()
}

function updateShowFields(updatedShowFields: { show: boolean, value: string }[]) {
    showFields.value = [...updatedShowFields]
}

const samples = ref<SampleModel[]>([])
const total = ref(0)
const errorMessage = ref('')
const isLoading = ref(false)
const offset = ref(1 + sampleStore.pagination.offset)

onMounted(async () => {
    if (!schemaStore.schema.project_id) {
        const { data } = await ProjectService.getProject(props.projectId)
        schemaStore.schema = {
            ...data
        }
    }
    handleSubmit()
})

function tsvUpload() {

}

function handleSubmit() {
    sampleStore.resetPagination()
    offset.value = 1
    const { filters, ...sortFields } = sampleStore.searchForm
    const validFilters = Object.fromEntries(Object.entries(filters).filter(([k, v]) => v))
    getSamples({ ...validFilters, ...sortFields, ...sampleStore.pagination })
}

function handlePagination(value: number) {
    sampleStore.pagination.offset = value - 1
    getSamples({ ...sampleStore.searchForm, ...sampleStore.pagination })
}

function editSample(index: number) {
    sampleStore.sample = { ...samples.value[index] }
    sampleStore.showForm = !sampleStore.showForm
}

async function deleteSample(index: number) {
    try {
        const sampleToDelete = samples.value[index]
        const { data } = await SampleService.deleteSample(props.projectId, sampleToDelete.sample_id)
        toast({ message: data.message, color: 'success', duration: 1500 })
    } catch (error) {
        toast({ message: 'Error', color: 'danger', duration: 1500 })
    } finally {
        reset()
    }
}

async function reset() {
    offset.value = 1
    sampleStore.resetSeachForm()
    sampleStore.resetPagination()
    handleSubmit()
}

async function getSamples(query: Record<string, any>) {
    try {
        const { data } = await SampleService.getSamples(schemaStore.schema.project_id, query)
        samples.value = data.data
        total.value = data.total
    } catch (e) {
        errorMessage.value = 'Something happened'
    } finally {
        isLoading.value = false
    }
}
</script>
