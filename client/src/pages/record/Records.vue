<template>
    <div class="row row-equal">
        <div class="flex lg3 md5 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <div class="row align-center justify-space-between">
                        <div class="flex">
                            <h2 class="va-h6">
                                Filters
                            </h2>
                        </div>
                        <div class="flex">
                            <VaButton @click="handleReset" :disabled="activeFilters.length === 0" color="textPrimary"
                                preset="secondary">
                                Clear all
                            </VaButton>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <Search :model="model" :project-id="projectId" />
                </VaCardContent>
                <VaCardContent>
                    <Filters :project-id="projectId" :model="model" />
                </VaCardContent>
            </VaCard>
        </div>
        <div class="flex lg9 md7 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <TableActions />
                </VaCardContent>
                <VaCardContent>
                    <VaCard square outlined color="backgroundPrimary">
                        <DataTable :project-id="projectId" :model="model"></DataTable>
                    </VaCard>
                </VaCardContent>
                <VaCardContent>
                    <div class="row justify-center">
                        <div class="flex">
                            <div class="row justify-center">
                                <div class="flex">
                                    <VaPagination color="textPrimary" v-model="offset"
                                        @update:modelValue="handlePagination" :page-size="recordStore.pagination.limit"
                                        :total="total" :visible-pages="3" buttons-preset="primary" gapped />
                                </div>
                            </div>
                        </div>
                    </div>
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
import { computed, watch } from 'vue';
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


const total = computed(() => recordStore.total)

const offset = computed({
    get() {
        return recordStore.pagination.offset + 1
    }, set(v: number) {
        recordStore.pagination.offset = v - 1
    }
})

const activeFilters = computed(() => Object.values(recordStore.searchForm).map(value => Object.values(value)).flat().filter(v => v))
async function handlePagination() {
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

async function handleReset() {
    recordStore.resetSearchForm()
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

</script>
