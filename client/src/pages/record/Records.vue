<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <Search :model="model" :project-id="projectId" />
                </VaCardContent>
                <VaDivider style="margin: 0;" />
                <Filters :project-id="projectId" :model="model" />
                <VaDivider v-if="recordStore.showFilters" style="margin: 0;" />
                <VaCardContent>
                    <TableActions />
                </VaCardContent>
                <VaCardContent>
                    <DataTable :project-id="projectId" :model="model"></DataTable>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <ChartCreation :project-id="projectId" :model="model" />
    <RecordDetailsModal :reference-model="model.reference_model" />
    <RecordFormModal :model="model" :project-id="projectId" :reference-model="model.reference_model" />
    <DeleteModal :project-id="projectId" :model-name="model.name" />
    <TSVExport :model-name="model.name" :project-id="projectId" />
</template>
<script setup lang="ts">
import { watch } from 'vue';
import { useRecordStore } from '../../stores/record-store';
import { ReseachModel } from '../../data/types';
import TSVExport from './components/TSVExport.vue';
import Search from './components/Search.vue';
import Filters from './components/Filters.vue';
import DeleteModal from './components/DeleteModal.vue';
import RecordFormModal from './components/RecordFormModal.vue';
import TableActions from './components/TableActions.vue';
import DataTable from './components/DataTable.vue';
import RecordDetailsModal from './components/RecordDetailsModal.vue';
import ChartCreation from './components/ChartCreation.vue';

const props = defineProps<{
    projectId: string,
    model: ReseachModel
}>()

const recordStore = useRecordStore()

watch(() => props.model, async () => {
    recordStore.resetSearchForm()
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}, { immediate: true })

</script>
