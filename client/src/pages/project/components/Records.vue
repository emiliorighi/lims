<template>
    <div class="row justify-space-between">
        <div class="flex lg6 md8 sm12 xs12">
            <VaInput v-model="recordStore.searchForm.filter" @update:modelValue="handleSearch" clearable
                placeholder="Search by identifier">
                <template #prependInner>
                    <VaIcon name="fa-search" />
                </template>
            </VaInput>
        </div>
        <div class="flex">
            <div class="row">
                <div class="flex">
                    <VaButton color="textPrimary" preset="primary" icon="fa-filter">Filter
                    </VaButton>
                </div>
                <div class="flex">
                    <VaMenu>
                        <template #anchor>
                            <VaButton color="textPrimary" preset="primary" icon="fa-sliders">
                                Actions
                            </VaButton>
                        </template>
                        <VaMenuItem @selected="toggleForm" icon="fa-plus">
                            Create Record
                        </VaMenuItem>
                        <VaMenuItem @selected="recordStore.showReportModal = true" icon="fa-file-export">
                            Export TSV
                        </VaMenuItem>
                        <VaMenuItem icon="fa-chart-simple">
                            Generate Chart
                        </VaMenuItem>
                    </VaMenu>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaDataTable :loading="recordStore.tableLoading" :items="records" :columns="columns"
                @columnSorted="sortItems" hoverable>
                <template #cell(reference_id)="{ rowData }">
                    <VaChip size="small" outline>
                        {{ rowData.reference_id }}
                    </VaChip>
                </template>
                <template #header(actions)>

                </template>
                <template #cell(actions)="{ rowData, row, isExpanded }">
                    <div class="row justify-end">
                        <div class="flex">
                            <VaChip :icon="isExpanded ? 'va-arrow-up' : 'va-arrow-down'" @click="row.toggleRowDetails()"
                                size="small">
                                {{ isExpanded ? 'hide' : 'view' }}
                            </VaChip>
                        </div>
                        <div class="flex">
                            <VaChip color="secondary" v-if="canBeEdited" @click="editItem(rowData)" size="small"
                                icon="fa-edit">
                                edit
                            </VaChip>
                        </div>
                        <div class="flex">
                            <VaChip @click="triggerDeleteItem(rowData)" size="small" color="danger" icon="fa-close">
                                delete
                            </VaChip>
                        </div>
                    </div>
                </template>
                <template #expandableRow="{ rowData }">
                    <RecordDetails :record="rowData" />
                </template>
            </VaDataTable>
        </div>
    </div>
    <VaDivider style="margin: 0;" />
    <div class="row justify-space-between align-center">
        <div class="flex va-text-secondary">
            Number of records: {{ total }}
        </div>
        <div class="flex">
            <VaPagination color="textPrimary" v-model="offset" @update:modelValue="handlePagination"
                :page-size="recordStore.pagination.limit" :total="total" :visible-pages="3" buttons-preset="primary"
                gapped />
        </div>
    </div>
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

const props = defineProps<{
    projectId: string,
    model: ReseachModel
}>()

const uneditableFields = ['item_id', 'project_id', 'model_name', 'created', '_id']

const globalStore = useGlobalStore()
const recordStore = useRecordStore()
const { init } = useToast()
const deleteLoading = ref(false)
const showDeleteConfirmation = ref(false)
const idToDelete = ref<null | string>(null)
const offset = ref(0)
const relatedRecords = ref<ResearchRecord[]>([])
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

async function handleSearch(filter: string) {
    recordStore.searchForm.filter = filter
    resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

function editItem(item: ResearchRecord) {
    const filteredEntries = Object.entries(item).filter(([k, v]) => !uneditableFields.includes(k))
    recordStore.setForm(item.item_id, Object.fromEntries(filteredEntries))
    recordStore.showRecordForm = true
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

function toggleForm() {
    recordStore.showRecordForm = true
}

async function getRelatedRecords(itemId: string) {

    const { data } = await RecordService.getRelatedRecords(props.projectId, props.model.name, itemId, {})
    relatedRecordsCount.value = data.total

}


</script>