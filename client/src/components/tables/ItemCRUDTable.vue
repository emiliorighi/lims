<template>
    <VaDataTable :items="items" :columns="mapColumns">
        <template #cell(actions)="{ rowIndex }">
            <VaButton v-if="canBeEdited(items[rowIndex])" preset="plain" icon="edit"
                @click="$emit('editClicked', rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3"
                @click="triggerDeleteConfirm(rowIndex)" />
        </template>
        <template #cell(sample_id)="{ rowIndex }">
            <VaChip @click="emits('showSampleDetails', items[rowIndex].sample_id)" color="textPrimary" flat> {{
        items[rowIndex].sample_id }}</VaChip>
        </template>
        <template #cell(experiment_id)="{ rowIndex }">
            <VaChip @click="emits('showExperimentDetails', items[rowIndex].experiment_id)" color="textPrimary" flat> {{
        items[rowIndex].experiment_id
    }}</VaChip>
        </template>
    </VaDataTable>
    <VaModal v-model="confirmDelete" hide-default-actions>
        <template #header>
            <div class="row align-center justify-space-between">
                <div class="flex">
                    <h3 class="va-h3">
                        Deleting {{ idToDelete }}? </h3>
                    <p class="va-text-secondary">
                        This will permanently delete the object
                    </p>
                </div>
            </div>
        </template>
        <VaDivider />
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

const emits = defineEmits(['editClicked', 'deleteClicked', 'showSampleDetails', 'showExperimentDetails'])

const confirmDelete = ref(false)
const props = defineProps<{
    columns: string[]
    items: Record<string, any>[],
}>()

const idToDelete = ref('')
const indexToDelete = ref(0)

function canBeEdited(rowData: Record<string, any>) {
    let modelType: 'sample' | 'experiment' = rowData.experiment_id ? 'experiment' : 'sample'
    const { id_format, fields } = schemaStore.schema[modelType]
    const optionalFields = fields.filter(f => !f.required)
    return id_format.length !== Object.keys(rowData.metadata).length || optionalFields.length
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