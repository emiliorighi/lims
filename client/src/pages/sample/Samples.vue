<template>
    <div>
        <div class="row justify-space-between align-end">
            <div class="flex">
                <h1 class="va-h1">List of Samples</h1>
                <p style="margin-bottom: 6px" class="va-text-secondary">Samples of {{ schemaStore.schema.project_id }}
                </p>
            </div>
            <div class="flex">
                <VaMenu>
                    <template #anchor>
                        <VaButton>Actions</VaButton>
                    </template>
                    <VaMenuItem icon="add"
                        @selected="router.push({ name: 'sample-form', params: { projectId: schemaStore.schema.project_id } })">
                        Create Sample
                    </VaMenuItem>
                    <VaMenuItem icon="upload"
                        @selected="router.push({ name: 'sample-upload', params: { projectId: schemaStore.schema.project_id } })">
                        Upload Samples
                    </VaMenuItem>
                    <VaMenuItem icon="download" @selected="showModal = !showModal">
                        Download Report
                    </VaMenuItem>
                </VaMenu>
            </div>
        </div>
        <div v-if="schemaStore.schema.project_id" class="row row-equal">
            <VaDivider />
            <div class="flex lg12 md12 sm12 xs12">
                <VaCard>
                    <VaCardContent>
                        <div class="row justify-space-between">
                            <div class="flex">
                                <TableFilters @on-metadata-update="updateQueryForm" @on-search-change="updateSearchForm"
                                    :columns="columns" :fields="schemaStore.schema.sample.fields"
                                    @on-show-field-change="updateShowFields" />
                            </div>
                            <div class="flex">
                                <Pagination @offset-changed="handlePagination" :limit="sampleStore.pagination.limit"
                                    :offset="sampleStore.pagination.offset" :total="total" />
                            </div>
                        </div>
                    </VaCardContent>
                    <VaCardContent>
                        <CRUDTable :items="samples" :columns="columns" @edit-clicked="editSample"
                            @delete-clicked="deleteSample" />
                    </VaCardContent>
                    <VaDivider />
                    <VaCardContent>
                        <div class="row justify-center">
                            <div class="flex">
                                <Pagination @offset-changed="handlePagination" :limit="sampleStore.pagination.limit"
                                    :offset="sampleStore.pagination.offset" :total="total" />
                            </div>
                        </div>
                    </VaCardContent>
                </VaCard>
                <va-modal v-model="showModal" hide-default-actions title="Download TSV Report">
                    <va-inner-loading :loading="isTSVLoading">
                        <div class="row">
                            <VaSelect class="flex lg12 md12 sm12 xs12" v-model="downloadFields"
                                searchPlaceholderText="Type to search" label="Columns"
                                :options="schemaStore.schema.sample.fields.map(f => f.key)" placeholder="Column list"
                                multiple :messages="['Search fields to use as TSV columns']" />
                        </div>
                        <div class="row">
                            <div class="flex lg12 md12 sm12 xs12">
                                <VaCheckbox style="margin-top: 6px;" v-model="applyFilters"
                                    label="Apply current filter">
                                </VaCheckbox>
                            </div>
                        </div>
                    </va-inner-loading>
                    <template #footer>
                        <va-button @click="downloadData"> Submit</va-button>
                    </template>
                </va-modal>
            </div>
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
import ProjectService from '../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';

const props = defineProps<{
    projectId: string
}>()

const router = useRouter()
const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { toast } = useGlobalStore()

const downloadFields = ref<string[]>([])
const showModal = ref(false)
const isTSVLoading = ref(false)
const applyFilters = ref(true)

const mappedFields = schemaStore.schema.sample.fields.map((f: Filter) => { return { show: f.required, value: f.key } })

const showFields = ref(mappedFields)

const columns = computed(() => {
    return ['sample_id', ...showFields.value.filter(f => f.show).map(f => `metadata.${f.value}`), 'actions']
})

function updateSearchForm(tuple: ['filter' | 'sort_column' | 'sort_order', Record<string, any>[keyof Record<string, any>]]) {
    const store = { ...sampleStore.searchForm }
    store[tuple[0]] = tuple[1]
    sampleStore.searchForm = { ...store }
    handleSubmit()
}


function updateQueryForm(list: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {
    const { query, ...otherFields } = sampleStore.searchForm
    const newQuery = { query: { ...query, ...Object.fromEntries(list) } }
    sampleStore.searchForm = { ...otherFields, ...newQuery }

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
        await fetchSchema(props.projectId)
    }
    await handleSubmit()
})

async function fetchSchema(projectId: string) {
    try {
        const { data } = await ProjectService.getProject(projectId)
        schemaStore.schema = {
            ...data
        }
    } catch (error) {
        console.error(error)
        toast({ message: 'Error Fetching project', color: 'danger', duration: 1500 })
    } finally {
    }
}

async function handleSubmit() {
    sampleStore.resetPagination()
    offset.value = 1
    const { query, ...fields } = sampleStore.searchForm
    // console.log(query)
    const validFilters = Object.fromEntries(Object.entries(query).filter(([k, v]) => v))
    await getSamples({ ...validFilters, ...fields, ...sampleStore.pagination })
}

async function handlePagination(value: number) {
    sampleStore.pagination.offset = value - 1
    await getSamples({ ...sampleStore.searchForm, ...sampleStore.pagination })
}

function editSample(index: number) {
    router.push({
        name: 'sample-form-update',
        params: {
            projectId: schemaStore.schema.project_id,
            sampleId: samples.value[index].sample_id
        }
    })
}

async function deleteSample(index: number) {
    try {
        const sampleToDelete = samples.value[index]
        const { data } = await SampleService.deleteSample(props.projectId, sampleToDelete.sample_id)
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
        errorMessage.value = 'Something happened'
    } finally {
        isLoading.value = false
    }
}

async function downloadData() {
    const downloadRequest = { format: "tsv", fields: [...downloadFields.value] }
    try {
        isTSVLoading.value = true
        const requestData = applyFilters.value ? {
            filter: sampleStore.searchForm.filter,
            sort_column: sampleStore.searchForm.sort_column, sort_order: sampleStore.searchForm.sort_order,
            ...sampleStore.searchForm.query,
            ...downloadRequest
        }
            :
            { ...downloadRequest }

        const response = await SampleService.getTsv(props.projectId, requestData)
        const data = response.data
        const href = URL.createObjectURL(data);

        const filename = 'sample_report.tsv'
        // create "a" HTML element with href to file & click
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', filename); //or any other extension
        document.body.appendChild(link);
        link.click();
        // clean up "a" element & remove ObjectURL
        document.body.removeChild(link);
        URL.revokeObjectURL(href);

    } catch (e) {

        const axiosError = e as AxiosError
        toast({ message: axiosError.message, color: 'danger' })

    } finally {
        isTSVLoading.value = false
        showModal.value = !showModal.value
    }
}

</script>
