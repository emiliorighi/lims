<template>
    <va-data-table :items="items" :columns="columns">
        <template #cell(sample_id)="{ rowData }">
            <VaChip outline
                :to="{ name: 'sample', params: { projectId: schemaStore.schema.project_id, sampleId: rowData.sample_id } }">
                {{ rowData.sample_id }}
            </VaChip>
        </template>
        <template #cell(experiment_id)="{ rowData }">
            <VaChip outline>
                {{ rowData.experiment_id }}
            </VaChip>
        </template>
        <template #cell(actions)="{ rowIndex }">
            <VaButton v-if="canBeEdited(items[rowIndex])" preset="plain" icon="edit"
                @click="$emit('editClicked', rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3"
                @click="$emit('deleteClicked', rowIndex)" />
        </template>
    </va-data-table>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';


const schemaStore = useSchemaStore()

const emits = defineEmits(['editClicked', 'deleteClicked', 'newClicked'])
const props = defineProps<{
    columns: string[]
    items: Record<string, any>[],
}>()


function canBeEdited(rowData: Record<string, any>) {
    let modelType: 'sample' | 'experiment' = rowData.sample_id ? 'sample' : 'experiment'
    const { id_format } = schemaStore.schema[modelType]
    return id_format.length === Object.keys(rowData.metadata).length
}

</script>