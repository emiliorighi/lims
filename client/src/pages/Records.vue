<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <div class="row align-center justify-space-between">
                <div class="flex lg4 md6 sm12 xs12">
                    <VaInput v-model="filter" @update:model-value="debouncedSearch" placeholder="Search records..."
                        clearable>
                        <template #appendInner>
                            <VaButton style="margin-left: 3px;" preset="secondary" icon="help"
                                @click="showQueryInfo = !showQueryInfo" />
                        </template>
                    </VaInput>
                </div>
                <div class="flex">
                    <div class="row">
                        <div v-if="hasFilters" class="flex">
                            <VaButton icon="fa-filter" color="textPrimary"
                                @click="recordStore.showFilters = !recordStore.showFilters" preset="primary">
                                {{ recordStore.showFilters ? 'Hide' : 'Show' }} Filters</VaButton>
                        </div>
                        <div class="flex">
                            <VaButton :disabled="isArchived"
                                @click="recordStore.showRecordForm = !recordStore.showRecordForm" icon="fa-plus">New
                                record</VaButton>
                        </div>
                        <div class="flex">
                            <VaButton :disabled="isArchived"
                                @click="recordStore.showTSVImportModal = !recordStore.showTSVImportModal"
                                preset="primary" icon="fa-file-import">Import TSV</VaButton>
                        </div>
                        <div class="flex">

                            <VaMenu>
                                <template #anchor>
                                    <VaButton color="textPrimary" preset="primary">Export</VaButton>
                                </template>
                                <VaMenuItem @selected="recordStore.showReportModal = !recordStore.showReportModal"
                                    icon="fa-file-export">
                                    Export TSV
                                </VaMenuItem>
                                <VaMenuItem @selected="recordStore.showChartModal = !recordStore.showChartModal"
                                    icon="fa-chart-simple">
                                    Export chart
                                </VaMenuItem>

                            </VaMenu>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="recordStore.showFilters" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard color="backgroundElement">
                        <VaCardContent>
                            <div class="row">
                                <div class="flex">
                                    <h3 class="va-h6">Filters</h3>
                                </div>
                            </div>
                            <div class="row align-center">
                                <div v-for="filter in queryFilters" class="flex lg3 md4 sm6 xs6">
                                    <FilterField :key="filter.key" @update-query="handleUpdate" :field="filter"
                                        :project-id="projectId" :model-name="modelName">
                                    </FilterField>
                                </div>
                                <div v-if="refModelFilter" class="flex lg3 md4 xs6 sm6">
                                    <FilterField :key="refModelFilter.key" @update-query="handleUpdate"
                                        :field="refModelFilter" :project-id="projectId" :model-name="modelName" />
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>
            <div v-if="activeFilters.length" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard color="backgroundElement">
                        <VaCardContent>
                            <div class="row justify-space-between">
                                <div class="flex va-text-bold">
                                    <h3 class="va-h6">Active Filters</h3>
                                </div>
                                <div class="flex">
                                    <VaButton color="textPrimary" preset="primary" @click="handleReset">Clear
                                        Filters</VaButton>
                                </div>
                            </div>
                        </VaCardContent>
                        <VaCardContent>
                            <div class="row">
                                <div v-for="[k, v] in activeFilters" class="flex">
                                    <VaChip outline @click="handleUpdate({ key: k as string, query: {} })"
                                        icon="fa-close">
                                        {{ k }}: {{ v }}
                                    </VaChip>
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard>
                        <VaCardContent>

                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaDataTable :loading="recordStore.tableLoading" :items="records" :columns="columns"
                                        @columnSorted="sortItems" hoverable>
                                        <template #cell(reference_id)="{ rowData }">
                                            <VaButton @click="showRelatedRecord(rowData.reference_id)"
                                                color="textPrimary" preset="secondary"
                                                icon-right="fa-up-right-from-square">
                                                {{ rowData.reference_id }}
                                            </VaButton>
                                        </template>
                                        <template #cell(actions)="{ rowData }">
                                            <div style="min-width: 300px;" class="row">
                                                <div class="flex">
                                                    <VaChip size="small" @click="viewItem(rowData)"
                                                        color="backgroundElement">
                                                        View
                                                    </VaChip>
                                                </div>
                                                <div v-if="canBeEdited && !isArchived" class="flex">
                                                    <VaChip size="small" @click="editItem(rowData)">Edit
                                                    </VaChip>
                                                </div>
                                                <div class="flex">
                                                    <VaChip v-if="!isArchived" size="small"
                                                        @click="triggerDeleteItem(rowData)" color="danger">
                                                        Delete
                                                    </VaChip>
                                                </div>
                                            </div>
                                        </template>
                                    </VaDataTable>
                                </div>
                            </div>
                            <div class="row justify-space-between align-center">
                                <div class="flex">
                                    Results: {{ total }}
                                </div>
                                <div class="flex">
                                    <div class="row justify-center">
                                        <div class="flex">
                                            <VaPagination v-model="offset" @update:modelValue="handlePagination"
                                                :page-size="recordStore.pagination.limit" :total="total"
                                                :visible-pages="3" buttons-preset="primary" gapped />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </VaCardContent>

                    </VaCard>
                </div>
            </div>
            <!-- <VaCard>
                <VaCardContent>
                    <div class="row align-center justify-space-between">
                        <div class="flex">
                            <VaInput v-model="filter" @update:model-value="debouncedSearch"
                                placeholder="Search by indentifier" clearable>
                                <template #appendInner>
                                    <VaButton style="margin-left: 3px;" preset="secondary" icon="help"
                                        @click="showQueryInfo = !showQueryInfo" />
                                </template>
                            </VaInput>
                        </div>
                        <div class="flex">
                            <div class="row">
                                <div v-if="hasFilters" class="flex">
                                    <VaButton icon="fa-filter" color="textPrimary"
                                        @click="recordStore.showFilters = !recordStore.showFilters" preset="primary">
                                        {{ recordStore.showFilters ? 'Hide' : 'Show' }} Filters</VaButton>
                                </div>
                                <div class="flex">
                                    <VaMenu>
                                        <template #anchor>
                                            <VaButton>Actions</VaButton>
                                        </template>
                                        <VaMenuItem :disabled="isArchived"
                                            @selected="recordStore.showRecordForm = !recordStore.showRecordForm"
                                            icon="fa-plus">
                                            Create new record
                                        </VaMenuItem>
                                        <VaMenuItem :disabled="isArchived"
                                            @selected="recordStore.showTSVImportModal = !recordStore.showTSVImportModal"
                                            icon="fa-file-import">
                                            Import records from TSV
                                        </VaMenuItem>
                                        <VaMenuItem
                                            @selected="recordStore.showReportModal = !recordStore.showReportModal"
                                            icon="fa-file-export">
                                            Export records in TSV
                                        </VaMenuItem>
                                        <VaMenuItem @selected="recordStore.showChartModal = !recordStore.showChartModal"
                                            icon="fa-chart-simple">
                                            Export chart
                                        </VaMenuItem>

                                    </VaMenu>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row justify-space-between align-center">
                        <div class="flex">
                            Results: {{ total }}
                        </div>
                        <div class="flex">
                            <div class="row justify-center">
                                <div class="flex">
                                    <VaPagination v-model="offset" @update:modelValue="handlePagination"
                                        :page-size="recordStore.pagination.limit" :total="total" :visible-pages="3"
                                        buttons-preset="primary" gapped />
                                </div>
                            </div>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent v-if="recordStore.showFilters">
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaCard color="backgroundElement">
                                <VaCardContent>
                                    <div class="row">
                                        <div class="flex">
                                            <h3 class="va-h6">Filters</h3>
                                        </div>
                                    </div>
                                    <div class="row align-center">
                                        <div v-for="filter in queryFilters" class="flex lg3 md4 sm6 xs6">
                                            <FilterField :key="filter.key" @update-query="handleUpdate" :field="filter"
                                                :project-id="projectId" :model-name="modelName">
                                            </FilterField>
                                        </div>
                                        <div v-if="refModelFilter" class="flex lg3 md4 xs6 sm6">
                                            <FilterField :key="refModelFilter.key" @update-query="handleUpdate"
                                                :field="refModelFilter" :project-id="projectId"
                                                :model-name="modelName" />
                                        </div>
                                    </div>
                                </VaCardContent>
                            </VaCard>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent v-if="activeFilters.length">
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaCard color="backgroundElement">
                                <VaCardContent>
                                    <div class="row justify-space-between">
                                        <div class="flex va-text-bold">
                                            <h3 class="va-h6">Active Filters</h3>
                                        </div>
                                        <div class="flex">
                                            <VaButton color="textPrimary" preset="primary" @click="handleReset">Clear
                                                Filters</VaButton>
                                        </div>
                                    </div>
                                </VaCardContent>
                                <VaCardContent>
                                    <div class="row">
                                        <div v-for="[k, v] in activeFilters" class="flex">
                                            <VaChip outline @click="handleUpdate({ key: k as string, query: {} })"
                                                icon="fa-close">
                                                {{ k }}: {{ v }}
                                            </VaChip>
                                        </div>
                                    </div>
                                </VaCardContent>
                            </VaCard>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaDataTable :loading="recordStore.tableLoading" :items="records" :columns="columns"
                                @columnSorted="sortItems" hoverable>
                                <template #cell(reference_id)="{ rowData }">
                                    <VaButton @click="showRelatedRecord(rowData.reference_id)" color="textPrimary"
                                        preset="secondary" icon-right="fa-up-right-from-square">
                                        {{ rowData.reference_id }}
                                    </VaButton>
                                </template>
                                <template #cell(actions)="{ rowData }">
                                    <div style="min-width: 300px;" class="row">
                                        <div class="flex">
                                            <VaChip size="small" @click="viewItem(rowData)" color="backgroundElement">
                                                View
                                            </VaChip>
                                        </div>
                                        <div v-if="canBeEdited && !isArchived" class="flex">
                                            <VaChip size="small" @click="editItem(rowData)">Edit
                                            </VaChip>
                                        </div>
                                        <div class="flex">
                                            <VaChip v-if="!isArchived" size="small" @click="triggerDeleteItem(rowData)"
                                                color="danger">
                                                Delete
                                            </VaChip>
                                        </div>
                                    </div>
                                </template>
                            </VaDataTable>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <div class="row justify-space-between align-center">
                        <div class="flex">
                            Results: {{ total }}
                        </div>
                        <div class="flex">
                            <div class="row justify-center">
                                <div class="flex">
                                    <VaPagination v-model="offset" @update:modelValue="handlePagination"
                                        :page-size="recordStore.pagination.limit" :total="total" :visible-pages="3"
                                        buttons-preset="primary" gapped />
                                </div>
                            </div>
                        </div>
                    </div>
                </VaCardContent>
            </VaCard> -->
        </div>
    </div>
    <VaModal v-model="showQueryInfo">
        <template #header>
            <h3 class="va-h3">
                Record identifier filter
            </h3>
            <p class="va-text-secondary">This input filters by the formatted identifier of {{ modelName
            }} that is
                composed by
                the
                following fields:</p>
        </template>
        <div class="layout va-gutter-3 fluid">
            <div class="row">
                <div v-for="idField in idFormat" :key="idField" class="flex">
                    <VaChip color="textPrimary">{{ idField }}</VaChip>
                </div>
            </div>
        </div>
    </VaModal>
    <RecordDeleteModal :project-id="projectId" :model-name="modelName" />
    <ChartCreationModal :project-id="projectId" :modelName="modelName" :fields="fields" />
    <RecordDetailsModal :reference-model="refModel" />
    <RecordFormModal :model-name="modelName" :project-id="projectId" />
    <TSVExportModal :model-name="modelName" :project-id="projectId" />
    <TSVImportModal :model-name="modelName" :project-id="projectId" :ref-model="refModel" />

</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRecordStore } from '../stores/record-store';
import TSVExportModal from '../components/modals/TSVExportModal.vue';
import RecordFormModal from '../components//modals/RecordFormModal.vue';
import { InputType, ResearchFilter, ResearchRecord } from '../data/types';
import RecordDetailsModal from '../components/modals/RecordDetailsModal.vue';
import RecordDeleteModal from '../components/modals/RecordDeleteModal.vue';
import ChartCreationModal from '../components/modals/ChartCreationModal.vue';
import TSVImportModal from '../components/modals/TSVImportModal.vue';
import FilterField from '../components/filters/FilterField.vue';
import { useGlobalStore } from '../stores/global-store';
import { debounce } from '../composables/debounce';
import { useModelStore } from '../stores/model-store';
import { useProjectStore } from '../stores/project-store';

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

const uneditableFields = ['item_id', 'project_id', 'model_name', 'created', '_id']

const globalStore = useGlobalStore()
const recordStore = useRecordStore()
const projectStore = useProjectStore()
const modelStore = useModelStore()
const showQueryInfo = ref(false)
const total = computed(() => recordStore.total)
const isArchived = computed(() => projectStore.isArchived)
const offset = computed({
    get() {
        return recordStore.pagination.offset + 1
    }, set(v: number) {
        recordStore.pagination.offset = v - 1
    }
})
const filter = computed({
    get() {
        return recordStore.searchForm.filter?.filter ?? ""
    }, set(filter: string) {
        recordStore.searchForm.filter = { filter }
    }
})

const activeFilters = computed(() =>
    Object.entries(recordStore.searchForm)
        .filter(([k, v]) => Object.values(v).length)
        .map(([k, v]) => {
            if (Object.entries(v).length > 1) {
                const lte = `${k}__lte`
                const gte = `${k}__gte`
                return [k, `${v[gte]}-${v[lte]}`]
            }
            return [k, Object.values(v)[0]]
        }
        ))

const records = computed(() => recordStore.records)
const isAuthorized = computed(() => globalStore.user.role !== 'researcher')
const fields = computed(() => modelStore.filters)
const idFormat = computed(() => modelStore.idFormat)
const canBeEdited = computed(() => idFormat.value.length <= fields.value.length)
const mappedKeys = computed(() => fields.value.map(({ key }) => ({ key, sortable: true, label: key })))
const refModel = computed(() => modelStore.refModel)
const hasFilters = computed(() => fields.value && idFormat.value && fields.value.length > idFormat.value.length)
const columns = computed(() => {
    const keys = mappedKeys.value ?? []
    const c = [...keys]
    if (refModel.value) c.push({ key: 'reference_id', sortable: true, label: refModel.value.name })
    if (isAuthorized.value) c.push({ key: 'actions', sortable: false, label: '' })
    return c
})

const refModelFilter = computed(() => {
    if (refModel.value) {
        return {
            key: 'reference_id',
            type: 'text' as InputType,
            payload: recordStore.searchForm.reference_id ? recordStore.searchForm.reference_id : { [`reference_id__in`]: null }
        }
    }

})

const queryFilters = computed(() => fields.value?.map(({ key, type }) => {
    let payload = type === 'date' || type === 'number' ? { [key]: null } : { [`${key}__in`]: null }
    if (recordStore.searchForm[key]) {
        payload = recordStore.searchForm[key]
    }
    return { key, type, payload }
}))

watch(() => props.modelName, async () => {
    await handleReset()
    recordStore.showFilters = false
}, { immediate: true })


async function handleSearch(filter: string) {
    recordStore.searchForm.filter = { filter }
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.modelName)
}

const debouncedSearch = debounce(async (payload: any) => {
    await handleSearch(payload)
}, 200);


async function handlePagination() {
    await recordStore.fetchRecords(props.projectId, props.modelName)
}

async function handleUpdate(payload: { key: string, query: Record<string, any> }) {
    const { key, query } = payload
    recordStore.searchForm[key] = { ...query }
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.modelName)
}



async function handleReset() {
    recordStore.resetSearchForm()
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.modelName)
}

async function showRelatedRecord(recordId: string | undefined) {
    if (!recordId || !refModel.value) return
    await recordStore.fetchItem(props.projectId, refModel.value.name, recordId)
    console.log(recordStore.record)
    recordStore.showRecordDetails = true
}

async function sortItems(event: { columnName: string, value: 'asc' | 'desc' | null, column: any },) {
    const { columnName, value } = event
    recordStore.sort.sort_column = columnName
    recordStore.sort.sort_order = value
    await recordStore.fetchRecords(props.projectId, props.modelName)
}

function editItem(item: ResearchRecord) {
    const filteredEntries = Object.entries(item).filter(([k, v]) => !uneditableFields.includes(k))
    recordStore.setForm(item.item_id, Object.fromEntries(filteredEntries))
    recordStore.showRecordForm = true
}

async function triggerDeleteItem(item: ResearchRecord) {
    recordStore.idToDelete = item.item_id
    await recordStore.fetchRelatedRecords(props.projectId, props.modelName, item.item_id, {})
    recordStore.showDeleteConfirmation = true
}

function viewItem(item: ResearchRecord) {
    recordStore.record = { ...item }
    recordStore.showRecordDetails = true
}


</script>