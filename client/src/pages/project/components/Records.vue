<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex lg8 md8">
                            <div class="row">
                                <div class="flex lg8 md8">
                                    <DebounceInput @input="showFilters = false" icon="fa-search" :parent-model="filter"
                                        @change="handleSearch" :clearable="true" />
                                </div>
                                <div class="flex">
                                    <VaButton color="textPrimary" preset="primary" @click="showFilters = !showFilters"
                                        :icon="showFilters ? 'fa-filter-circle-xmark' : 'fa-filter'"> Filters
                                    </VaButton>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <VaButton style="margin-left: 3px;" preset="primary" color="textPrimary" icon="help"
                                @click="showQueryInfo = !showQueryInfo" />
                        </div>
                    </div>
                </VaCardContent>
                <VaDivider style="margin: 0;" />
                <VaCollapse v-model="showFilters">
                    <template #header>
                        <span></span>
                    </template>
                    <template #body>
                        <VaCardContent>
                            <div class="row align-center justify-space-between">
                                <div class="flex">
                                    <h2 class="va-h6">
                                        Filters
                                    </h2>
                                </div>
                            </div>
                            <div class="row">
                                <div v-for="field in model.fields" :key="field.key" class="flex lg6 md12 sm12 xs12">
                                    <FilterField :key="field.key" @update-query="handleUpdate" :field="field"
                                        :project-id="projectId" :model-name="model.name"
                                        :query="recordStore.searchForm[field.key]">
                                    </FilterField>
                                </div>
                            </div>
                            <div class="row justify-space-between">
                                <div class="flex">
                                    <VaButton @click="handleReset" color="danger">Reset Filters</VaButton>
                                </div>
                                <div class="flex">
                                    <VaButton :disabled="activeFilters.length === 0" @click="submitFilters"
                                        color="textPrimary">Apply Filters</VaButton>
                                </div>

                            </div>
                        </VaCardContent>
                    </template>
                </VaCollapse>
                <VaDivider v-if="showFilters" style="margin: 0;" />
                <VaCardContent>
                    <div class="row justify-space-between align-center">
                        <div class="flex">
                            <div class="row align-center">
                                <div class="flex">
                                    <h2 class="va-h6">
                                        Results
                                    </h2>
                                </div>
                                <div class="flex">
                                    <VaChip color="textPrimary" outline size="small">{{ total }}</VaChip>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <div class="row">
                                <div class="flex">
                                    <VaButton @click="recordStore.showRecordForm = !recordStore.showRecordForm"
                                        color="textPrimary" icon="fa-plus">
                                        New Record
                                    </VaButton>
                                </div>
                                <div class="flex">
                                    <VaMenu>
                                        <template #anchor>
                                            <VaButton color="textPrimary" preset="primary" icon-right="fa-caret-down">
                                                Actions</VaButton>
                                        </template>
                                        <VaMenuItem @selected="recordStore.showReportModal = true"
                                            icon="fa-file-export">
                                            Export TSV
                                        </VaMenuItem>
                                        <VaMenuItem icon="fa-chart-simple">
                                            Generate Chart
                                        </VaMenuItem>
                                    </VaMenu>
                                </div>
                                <div class="flex">
                                    <VaButtonGroup>
                                        <VaButton v-for="opt in options" color="textPrimary" @click="view = opt.value"
                                            :preset="view === opt.value ? undefined : 'primary'" :icon="opt.icon">
                                        </VaButton>
                                    </VaButtonGroup>
                                </div>
                            </div>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <div v-if="view === 'rows'" class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaDataTable :loading="recordStore.tableLoading" :items="records" :columns="columns"
                                @columnSorted="sortItems" hoverable>
                                <template #header="{ }"></template>
                                <template #header(reference_id)>
                                    {{ model.reference_model }}
                                </template>
                                <template #cell(reference_id)="{ rowData }">
                                    <VaButton color="textPrimary" preset="secondary"
                                        icon-right="fa-up-right-from-square">
                                        {{ rowData.reference_id }}
                                    </VaButton>
                                </template>
                                <template #header(actions)>
                                </template>
                                <template #cell(actions)="{ rowData }">
                                    <RecordActions :record="rowData" :disabled-edit="!canBeEdited"
                                        @delete="triggerDeleteItem" @edit="editItem" />
                                </template>
                            </VaDataTable>
                        </div>
                    </div>
                    <div class="row row-equal" v-else>
                        <div v-for="rec in records" :key="rec.item_id" class="flex lg4 md6 sm12 xs12">
                            <RecordDetails :disabled-actions="!isAuthorized" :disabled-edit="!canBeEdited"
                                @delete="triggerDeleteItem" :reference-model="model.reference_model" @edit="editItem"
                                :record="rec" />
                        </div>
                    </div>
                    <VaDivider style="margin: 0;" />
                    <div class="row justify-center">
                        <div class="flex">
                            <VaPagination color="textPrimary" v-model="offset" @update:modelValue="handlePagination"
                                :page-size="recordStore.pagination.limit" :total="total" :visible-pages="3"
                                buttons-preset="primary" gapped />
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <VaModal v-model="showQueryInfo">
        <template #header>
            <h3 class="va-h3">
                Record identifier filter
            </h3>
            <p class="va-text-secondary">This input filters by the formatted identifier of {{ model.name }} that is
                composed by
                the
                following fields:</p>
        </template>
        <div class="layout va-gutter-3 fluid">
            <div class="row">
                <div v-for="idField in model.id_format" :key="idField" class="flex">
                    <VaChip color="textPrimary">{{ idField }}</VaChip>
                </div>
            </div>
        </div>

    </VaModal>
    <VaModal v-model="showDeleteConfirmation" hide-default-actions>
        <template #header>
            <h3 class="va-h3">
                Deleting {{ idToDelete }}
            </h3>
            <p class="va-text-secondary">Deleting the item is irreversible, the linked data will be also deleted</p>
        </template>
        <VaDivider />
        <div class="row align-center justify-space-between">
            <div class="flex">
                <p class="va-text-danger">
                    This will permanently delete the object and its related records
                </p>
            </div>
        </div>
        <div v-if="relatedRecordsCount" class="row">
            <div class="flex">
                Related records: <VaChip style="margin-left: 3px;" flat size="large">
                    {{ relatedRecordsCount }}
                </VaChip>
            </div>
        </div>
        <template #footer>
            <VaButton :loading="deleteLoading" @click="deleteItem" color="danger">
                Confirm </VaButton>
        </template>
    </VaModal>
    <VaModal v-model="recordStore.showRecordDetails">

    </VaModal>
    <TSVExport :model-name="model.name" :project-id="projectId" />
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRecordStore } from '../../../stores/record-store';
import { ReseachModel, ResearchRecord } from '../../../data/types';
import { useGlobalStore } from '../../../stores/global-store';
import RecordDetails from '../../../components/record/RecordDetails.vue';
import RecordService from '../../../services/clients/RecordService';
import AuthService from '../../../services/clients/AuthService';
import { useToast } from 'vuestic-ui/web-components';
import { AxiosError } from 'axios';
import TSVExport from './TSVExport.vue';
import RecordActions from '../../../components/record/RecordActions.vue';
import FilterField from '../../../components/filters/FilterField.vue';
import DebounceInput from '../../../components/inputs/DebounceInput.vue';

const props = defineProps<{
    projectId: string,
    model: ReseachModel
}>()

const view = ref<'rows' | 'cards'>('rows')

const uneditableFields = ['item_id', 'project_id', 'model_name', 'created', '_id']
const showFilters = ref(false)
const options: { icon: string, value: 'rows' | 'cards' }[] = [
    { icon: 'list', value: 'rows' },
    { icon: 'grid_view', value: 'cards' },
]

// const

const globalStore = useGlobalStore()
const recordStore = useRecordStore()
const { init } = useToast()
const deleteLoading = ref(false)
const showDeleteConfirmation = ref(false)
const idToDelete = ref<null | string>(null)
const showQueryInfo = ref(false)
const offset = ref(0)
const relatedRecordsCount = ref(0)
const records = computed(() => recordStore.records)
const total = computed(() => recordStore.total)

const isAuthorized = computed(() => globalStore.user.role !== 'researcher')
const canBeEdited = computed(() => props.model.id_format.length < props.model.fields.length)
const mappedKeys = computed(() => props.model.fields.map(({ key }) => key))

const columns = computed(() => {
    const c = [...mappedKeys.value]
    if (props.model.reference_model) c.push('reference_id')
    if (isAuthorized.value) c.push('actions')
    return c
})

const filter = computed(() => recordStore.searchForm.filter ? recordStore.searchForm.filter?.filter : "")

const activeFilters = computed(() => Object.values(recordStore.searchForm).map(value => Object.values(value)).flat().filter(v => v))

watch(() => props.model, async () => {
    recordStore.resetSearchForm()
    resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}, { immediate: true })

function resetPagination() {
    offset.value = 0
    recordStore.resetPagination()
}

async function handlePagination(offset: number) {
    recordStore.pagination.offset = offset - 1
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

async function handleReset() {
    recordStore.resetSearchForm()
    resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}
async function handleSearch(filter: string) {
    recordStore.searchForm.filter = { filter }
    resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

function editItem(item: ResearchRecord) {
    const filteredEntries = Object.entries(item).filter(([k, v]) => !uneditableFields.includes(k))
    recordStore.setForm(item.item_id, Object.fromEntries(filteredEntries))
    recordStore.showRecordForm = true
}

function handleUpdate(payload: { key: string, query: Record<string, any> }) {
    const { key, query } = payload
    recordStore.searchForm[key] = { ...query }
}

async function submitFilters() {
    resetPagination()
    showFilters.value = false
    await recordStore.fetchRecords(props.projectId, props.model.name)

}
async function deleteItem() {
    try {
        deleteLoading.value = true
        const { data } = await AuthService.deleteRecord(props.projectId, props.model.name, idToDelete.value)
        init({ message: `Record ${idToDelete.value} and its related records ${relatedRecordsCount.value} have been deleted` })
    } catch (err) {
        const axiosError = err as AxiosError
        const responseData = axiosError.response?.data as { message: string }
        init({ message: responseData.message, color: 'danger' })
    } finally {
        deleteLoading.value = false
        idToDelete.value = null
        showDeleteConfirmation.value = false
        await handleSearch("")
    }

}

async function triggerDeleteItem(item: ResearchRecord) {
    idToDelete.value = item.item_id
    await getRelatedRecords(idToDelete.value)
    showDeleteConfirmation.value = true
}

async function sortItems(event: { columnName: string, value: 'asc' | 'desc' | null, column: any },) {
    const { columnName, value } = event
    recordStore.sort.sort_column = columnName
    recordStore.sort.sort_order = value
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

async function getRelatedRecords(itemId: string) {

    const { data } = await RecordService.getRelatedRecords(props.projectId, props.model.name, itemId, {})
    relatedRecordsCount.value = data.total

}


</script>
