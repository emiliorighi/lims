<template>
    <va-data-table :items="items" :columns="columns">
        <template #cell(sample_id)="{ rowData }">
            <RouterLink
                :to="{ name: 'sample', params: { projectId: schemaStore.schema.project_id, sampleId: rowData.sample_id } }">
                {{ rowData.sample_id }}
            </RouterLink>
        </template>
        <template #cell(experiment_id)="{ rowData }">
            <RouterLink
                :to="{ name: 'experiment', params: { projectId: schemaStore.schema.project_id, experimentId: rowData.experiment_id } }">
                {{ rowData.experiment_id }}
            </RouterLink>
        </template>
        <template #cell(actions)="{ rowIndex }">
            <VaButton v-if="canBeEdited(items[rowIndex])" preset="plain" icon="edit"
                @click="$emit('editClicked', rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3"
                @click="triggerDeleteConfirm(rowIndex)" />
        </template>
    </va-data-table>

    <VaModal v-model="confirmDelete" hide-default-actions overlay-opacity="0.2">
        <template #header>
            <h3>Are you sure you want to delete {{ idToDelete }}</h3>
        </template>
        <div>This will permanently delete the object</div>
        <template #footer>
            <VaButton @click="$emit('deleteClicked', indexToDelete); confirmDelete = !confirmDelete" color="danger">
                Confirm </VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { useSchemaStore } from '../../stores/schemas-store';
import { ref } from 'vue';


const schemaStore = useSchemaStore()

const emits = defineEmits(['editClicked', 'deleteClicked', 'newClicked'])

const confirmDelete = ref(false)
const props = defineProps<{
    columns: string[]
    items: Record<string, any>[],
}>()

const idToDelete = ref('')
const indexToDelete = ref(0)
function canBeEdited(rowData: Record<string, any>) {
    let modelType: 'sample' | 'experiment' = rowData.sample_id ? 'sample' : 'experiment'
    const { id_format } = schemaStore.schema[modelType]
    return id_format.length !== Object.keys(rowData.metadata).length
}


function triggerDeleteConfirm(index: number) {
    const item = props.items[index]
    idToDelete.value = item.sample_id || item.experiment_id
    indexToDelete.value = index
    confirmDelete.value = true
}

</script>