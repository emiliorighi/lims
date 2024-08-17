<template>
    <VaDataTable :items="items" :columns="columns">
        <template #cell(actions)="{ rowData }">
            <VaButton v-if="canBeEdited(rowData)" preset="plain" icon="edit" @click="editItem(rowData)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3" @click="triggerDelete(rowData)" />
        </template>
        <template #cell(sample_id)="{ rowData }">
            <VaChip @click="showItemDetails(rowData.sample_id, 'sample')" color="textPrimary" flat>
                {{ rowData.sample_id }}
            </VaChip>
        </template>
        <template #cell(experiment_id)="{ rowData }">
            <VaChip v-if="rowData.experiment_id" @click="showItemDetails(rowData.experiment_id, 'experiment')"
                color="textPrimary" flat>
                {{ rowData.experiment_id }}
            </VaChip>
        </template>
    </VaDataTable>
</template>

<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store'
import { ModelType } from '../../data/types'

const schemaStore = useSchemaStore()

const props = defineProps<{
    items: any[],
    columns: string[],
    model: ModelType,
}>();

const emit = defineEmits(['edit-item', 'trigger-delete', 'show-item-details']);

function editItem(rowData: any) {
    emit('edit-item', rowData);
}

function triggerDelete(rowData: any) {
    emit('trigger-delete', rowData);
}

function showItemDetails(id: string, model: string) {
    emit('show-item-details', { id, model });
}

const canBeEdited = (rowData: any) => {
    const idFormat = schemaStore.schema[props.model].id_format;
    const fields = schemaStore.schema[props.model].fields;
    const optionalFields = fields.filter(f => !f.required);

    return idFormat.length !== Object.keys(rowData.metadata).length || optionalFields.length;
};
</script>