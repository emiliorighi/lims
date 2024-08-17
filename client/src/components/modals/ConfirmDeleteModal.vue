<template>
    <VaModal v-model="itemStore.showDeleteConfirm" hide-default-actions>
        <template #header>

            <div class="row align-center justify-space-between">
                <h3 class=" flex va-h3">
                    Deleting {{ itemStore.idToDelete }}? </h3>
                <VaIcon color="primary" size="large" class="flex" :name="icon" />
            </div>
        </template>
        <VaDivider />
        <div class="row align-center justify-space-between">
            <div class="flex">
                <p class="va-text-danger">
                    This will permanently delete the object
                </p>
            </div>
        </div>
        <template #footer>
            <VaButton @click="deleteItem" color="danger">
                Confirm </VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { useItemStore } from '../../stores/item-store'
import { ModelType } from '../../data/types'
import { useSchemaStore } from '../../stores/schemas-store'

const schemaStore = useSchemaStore()
const props = defineProps<{
    icon: string
    model: ModelType
}>()

const itemStore = useItemStore()

async function deleteItem() {
    const { project_id } = schemaStore.schema
    await itemStore.deleteItem(project_id, props.model)
    itemStore.resetPagination()
    itemStore.resetSearchForm()
    await itemStore.fetchItems(project_id, props.model)
    itemStore.showDeleteConfirm = !itemStore.showDeleteConfirm
}

</script>