<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaDataTable :loading="recordStore.tableLoading" :items="records" :columns="columns"
                @columnSorted="sortItems" hoverable>
                <template #cell(reference_id)="{ rowData }">
                    <VaButton @click="showRelatedRecord(rowData.reference_id)" color="textPrimary" preset="secondary"
                        icon-right="fa-up-right-from-square">
                        {{ rowData.reference_id }}
                    </VaButton>
                </template>
                <template #cell(actions)="{ rowData }">
                    <RecordActions :record="rowData" :disabled-edit="!canBeEdited" :project-id="projectId"
                        :model-name="model.name" />
                </template>
            </VaDataTable>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useRecordStore } from '../../../stores/record-store';
import { ReseachModel } from '../../../data/types';
import { useGlobalStore } from '../../../stores/global-store';
import RecordActions from './RecordActions.vue';


const props = defineProps<{
    projectId: string,
    model: ReseachModel
}>()

const globalStore = useGlobalStore()
const recordStore = useRecordStore()
const records = computed(() => recordStore.records)

const isAuthorized = computed(() => globalStore.user.role !== 'researcher')
const canBeEdited = computed(() => props.model.id_format.length < props.model.fields.length)
const mappedKeys = computed(() => props.model.fields.map(({ key }) => ({ key, sortable: true, label: key })))

const columns = computed(() => {
    const c = [...mappedKeys.value]
    if (props.model.reference_model) c.push({ key: 'reference_id', sortable: true, label: props.model.reference_model })
    if (isAuthorized.value) c.push({ key: 'actions', sortable: false, label: '' })
    return c
})

async function showRelatedRecord(recordId: string | undefined) {
    if (!recordId || !props.model.reference_model) return
    await recordStore.fetchItem(props.projectId, props.model.reference_model, recordId)
    recordStore.showRecordDetails = true
}
async function sortItems(event: { columnName: string, value: 'asc' | 'desc' | null, column: any },) {
    const { columnName, value } = event
    recordStore.sort.sort_column = columnName
    recordStore.sort.sort_order = value
    await recordStore.fetchRecords(props.projectId, props.model.name)
}



</script>
