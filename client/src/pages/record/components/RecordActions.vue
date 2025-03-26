<template>
    <VaMenu>
        <template #anchor>
            <VaButton color="textPrimary" preset="secondary" icon="more_horiz">
            </VaButton>
        </template>
        <VaMenuItem icon="fa-view" @selected="viewItem(record)">
            View
        </VaMenuItem>
        <VaMenuItem icon="fa-edit" @selected="editItem(record)" v-if="!disabledEdit">
            Edit
        </VaMenuItem>
        <VaMenuItem icon="fa-close" @selected="triggerDeleteItem(record)">
            Remove
        </VaMenuItem>
    </VaMenu>
</template>
<script setup lang="ts">
import { ResearchRecord } from '../../../data/types';
import { useRecordStore } from '../../../stores/record-store';

const props = defineProps<{
    record: ResearchRecord
    disabledEdit: boolean,
    projectId: string,
    modelName: string
}>()

const recordStore = useRecordStore()
const emits = defineEmits(['delete', 'edit'])

const uneditableFields = ['item_id', 'project_id', 'model_name', 'created', '_id']

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