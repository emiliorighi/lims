<template>
    <VaDataTable :items="items" :columns="mapColumns">
        <template #cell(actions)="{ rowIndex }">
            <VaButton v-if="canBeEdited(items[rowIndex])" preset="plain" icon="edit"
                @click="$emit('editClicked', rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3"
                @click="triggerDeleteConfirm(rowIndex)" />
        </template>
    </VaDataTable>
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
import { useSchemaStore } from '../../stores/schemas-store';
import { computed, ref } from 'vue';


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
    let modelType: 'sample' | 'experiment' = rowData.experiment_id ? 'experiment' : 'sample'
    const { id_format } = schemaStore.schema[modelType]
    return id_format.length !== Object.keys(rowData.metadata).length
}



const mapColumns = computed(() => {
    return props.columns.map((v) => {
        if (v.includes('metadata.')) {
            return { key: v, label: v.split('.')[1] }
        }
        return { key: v, label: v }
    })
})

function triggerDeleteConfirm(index: number) {
    const item = props.items[index]
    idToDelete.value = item.experiment_id || item.sample_id
    indexToDelete.value = index
    confirmDelete.value = true
}

</script>