<template>
    <VaDataTable :loading="recordStore.tableLoading" :items="records" :columns="columns" hoverable>
        <template #header(reference_id)>
            <RecordHeaderCell :field="refFieldPayload" :model-name="modelName" :project-id="projectId" />
        </template>
        <template v-if="recordStore.showRecordForm" #bodyPrepend>
            <RecordForm :model-name="modelName" :project-id="projectId" @submit:success="handleSubmitSuccess" />
        </template>
        <template #cell(created)="{ rowData }">
            <VaChip size="small" color="backgroundElement">{{ formatDate(new Date(rowData.created.$date)) }}</VaChip>
        </template>
        <template #cell(reference_id)="{ rowData }">
            <span class="va-link"
                @click="recordStore.viewRelatedRecord(projectId, refModel?.name, rowData.reference_id)">
                {{ rowData.reference_id }}
            </span>
        </template>
        <template #cell(actions)="{ rowData }">
            <div style="min-width: 200px;" class="row">
                <div class="flex">
                    <VaChip size="small" @click="recordStore.viewRecord(rowData)">view</VaChip>

                </div>
                <div v-if="deleteEnabled && (role === 'admin' || role === 'project_manager' || role === 'data_manager')" class="flex">
                    <VaChip size="small" color="danger"
                        @click="recordStore.triggerDelete(projectId, modelName, rowData)">delete</VaChip>

                </div>
            </div>
        </template>
    
        <template v-for="field in queryFilters" :key="field.key" #[`header(${field.key})`]>
            <RecordHeaderCell :field="field" :project-id="projectId" :model-name="modelName" />
        </template>
        <template v-for="item in editableColumns" :key="item.key" #[`cell(${item.key})`]="{ value, row }">
            <RecordInputCell :edit-mode="editMode" :item="item" :value="value" :row="row" :project-id="projectId"
                :model-name="modelName" />
        </template>
    </VaDataTable>
</template>
<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { numberDateQueryOperators } from '../../data/types';
import { useGlobalStore } from '../../stores/global-store';
import { useModelStore } from '../../stores/model-store';
import { useProjectStore } from '../../stores/project-store';
import { useRecordStore } from '../../stores/record-store';
import RecordHeaderCell from '../cells/RecordHeaderCell.vue';
import RecordForm from '../forms/RecordForm.vue';
import RecordInputCell from '../cells/RecordInputCell.vue';
import { formatDate } from '../../composables/formatDate';

const props = defineProps<{
    projectId: string,
    modelName: string,
    editMode: boolean
}>()

onMounted(async () => {
    if (refModel.value) {
        await recordStore.fetchRefRecords(props.projectId, props.modelName)
    }
})



const globalStore = useGlobalStore()
const recordStore = useRecordStore()
const projectStore = useProjectStore()
const modelStore = useModelStore()
const role = computed(() => globalStore.user.role)
const deleteEnabled = computed(() => props.editMode && !projectStore.isArchived)
const refIdOptions = computed(() => recordStore.refRecords)
const refFieldPayload = computed(() => ({ key: 'reference_id', label: `Reference ${refModel.value?.name}`, type: 'select', choices: refIdOptions.value, payload: recordStore.searchForm?.reference_id ?? { ...operatorMap.select } }))
const records = computed(() => recordStore.records)
const isAuthorized = computed(() => globalStore.user.role !== 'researcher')
const fields = computed(() => modelStore.filters)
const idFormat = computed(() => modelStore.idFormat)
const mappedKeys = computed(() => fields.value.map(({ key, type }) => ({ key, label: key, type })))
const refModel = computed(() => modelStore.refModel)

const editableColumns = computed(() => fields.value.filter(({ key }) => !idFormat.value.includes(key)))

const queryFilters = computed(() =>
    fields.value?.map(({ key, type, choices }) => {
        const isIdField = idFormat.value.includes(key)
        // If the value already exists in the form, return it directly
        if (recordStore.searchForm[key]) {
            return { key, type, payload: recordStore.searchForm[key], choices, isIdField };
        }
        // Fetch the default operator payload based on type or fallback to "exists"
        const payload = operatorMap[type] ?? { [numberDateQueryOperators.gte]: null };
        return { key, type, payload, choices, isIdField };
    })
);

const columns = computed(() => {
    const keys = mappedKeys.value ?? []
    const c = []
    if (refModel.value) c.push({ key: 'reference_id', label: refModel.value.name })
    c.push(...keys)
    if (isAuthorized.value) c.push({ key: 'actions', label: '' })
    return c
})


async function handleSubmitSuccess() {
    recordStore.resetForm()
    recordStore.toggleRecordForm()
    await recordStore.fetchRecords(props.projectId, props.modelName)
    await modelStore.getStats(props.projectId, props.modelName)
    if (refModel.value) await recordStore.fetchRefRecords(props.projectId, props.modelName)
}

const operatorMap: Record<string, any> = {
    text: { contains: null },
    select: { in: null },
    number: { gte: null },
    date: { gte: null },
};

</script>