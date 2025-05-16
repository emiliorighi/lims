<template>
    <VaCard outlined>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h3 class="va-h5">
                        {{ modelName }}
                    </h3>
                    <p class="va-text-secondary">A total of {{ count }} records have
                        been found!
                    </p>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <VaButton @click="handleRecordsDelete" :loading="loading" icon="fa-trash" preset="primary"
                        color="danger">
                        Delete
                        Records
                    </VaButton>
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useRecordStore } from '../../stores/record-store';
import AuthService from '../../services/clients/AuthService';

const props = defineProps<{
    projectId: string
    modelName: string
    count: number
    columns: string[]
}>()

const loading = ref(false)
const recordStore = useRecordStore()

async function handleRecordsDelete() {
    try {
        loading.value = true
        await recordStore.downloadData(props.projectId, props.modelName, props.columns, false)
        const { data } = await AuthService.deleteRecords(props.projectId, props.modelName)
        recordStore.toast({ message: data, color: 'success' })
    } catch (err) {
        recordStore.catchError(err)
    } finally {
        loading.value = true
    }
}
</script>