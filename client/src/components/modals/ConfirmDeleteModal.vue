<template>
    <VaModal v-model="itemStore.showDeleteConfirm" hide-default-actions>
        <template #header>
            <Header :title="`Deleting ${itemStore.idToDelete}?`" :icon="icon" />
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
import Header from './common/Header.vue'

const props = defineProps<{
    icon: string,
    projectId:string
}>()

const itemStore = useItemStore()

async function deleteItem() {
    await itemStore.deleteItem(props.projectId)
    itemStore.resetPagination()
    itemStore.resetSearchForm()
    await itemStore.fetchItems(props.projectId)
    itemStore.showDeleteConfirm = !itemStore.showDeleteConfirm
}

</script>