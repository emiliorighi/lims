<template>
    <VaModal v-model="gStore.showDeleteConfirmation" hide-default-actions>
        <template #header>
            <Header :title="`Deleting ${idToDelete}?`" :icon="icon" />
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
            <VaButton @click="emits('confirmDelete')" color="danger">
                Confirm </VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import Header from './common/Header.vue'
import { useGlobalStore } from '../../stores/global-store'

const gStore = useGlobalStore()

const props = defineProps<{
    icon: string,
    idToDelete: string,
}>()

const emits = defineEmits(['confirmDelete'])

</script>