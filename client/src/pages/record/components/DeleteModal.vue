<template>
    <VaModal v-model="recordStore.showDeleteConfirmation" hide-default-actions>
        <template #header>
            <h3 class="va-h3">
                Deleting {{ idToDelete }}
            </h3>
            <p class="va-text-secondary">Deleting the item is irreversible, the linked data will be also deleted</p>
        </template>
        <VaDivider />
        <div class="row align-center justify-space-between">
            <div class="flex">
                <p class="va-text-danger">
                    This will permanently delete the object and its related records
                </p>
            </div>
        </div>
        <div v-if="count" class="row">
            <div class="flex">
                Related records: <VaChip style="margin-left: 3px;" flat size="large">
                    {{ count }}
                </VaChip>
            </div>
        </div>
        <template #footer>
            <VaButton :loading="loading" @click="deleteItem" color="danger">
                Confirm </VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRecordStore } from '../../../stores/record-store';
import AuthService from '../../../services/clients/AuthService';
import { AxiosError } from 'axios';
import { useToast } from 'vuestic-ui/web-components';

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

const { init } = useToast()
const recordStore = useRecordStore()
const idToDelete = computed(() => recordStore.idToDelete)
const count = computed(() => recordStore.relatedRecordCount)
const loading = ref(false)

async function deleteItem() {
    try {
        loading.value = true
        const { data } = await AuthService.deleteRecord(props.projectId, props.modelName, idToDelete.value)
        init({ message: `Record ${idToDelete.value} and its related records ${count.value} have been deleted` })
    } catch (err) {
        const axiosError = err as AxiosError
        const responseData = axiosError.response?.data as { message: string }
        init({ message: responseData.message, color: 'danger' })
    } finally {
        loading.value = false
        recordStore.showDeleteConfirmation = false
        recordStore.idToDelete = null
        recordStore.resetPagination()
        await recordStore.fetchRecords(props.projectId, props.modelName)
    }
}

</script>