<template>
    <div>
        <div class="row justify-space-between mb-4">
            <div class="flex">
                <div class="row">
                    <div class="flex">
                        <VaButton color="textPrimary" :disabled="isArchived" @click="recordStore.toggleImportModal"
                            icon="fa-file-import" preset="primary">Import TSV</VaButton>
                    </div>
                    <div class="flex">
                        <VaButton :disabled="isArchived" color="success" icon="fa-plus" @click="recordStore.toggleRecordForm">Add Record
                        </VaButton>
                    </div>
                    <div class="flex">
                        <VaPopover
                            message="Update records in real-time, every change is instantly saved to the database.">
                            <VaButton :disabled="isArchived" @click="toggleEditMode" :icon="editMode ? 'fa-close' : 'fa-edit'"
                                :color="editMode ? 'danger' : 'textPrimary'" preset="primary">
                                {{ editMode ? 'Exit Edit Mode' : 'Enable Edit Mode' }}</VaButton>
                        </VaPopover>
                    </div>
                </div>
            </div>
            <div class="flex">
                <div class="row">
                    <div class="flex">
                        <VaButton color="textPrimary" preset="secondary" @click="recordStore.toggleReportModal"
                            icon="fa-file-export">
                            Export TSV
                        </VaButton>
                    </div>
                    <div class="flex">
                        <VaButton color="textPrimary" preset="secondary" @click="recordStore.toggleChartModal"
                            icon="fa-chart-simple">
                            Export Chart
                        </VaButton>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <VaCard>
                    <VaCardContent>
                        <RecordDataTable :edit-mode="editMode" :project-id="projectId" :model-name="modelName" />
                    </VaCardContent>
                    <VaCardContent>
                        <div class="row justify-space-between align-center">
                            <div class="flex">
                                Results: {{ total }}
                            </div>
                            <div class="flex">
                                <VaPagination color="textPrimary" v-model="offset" @update:modelValue="handlePagination"
                                    :page-size="recordStore.pagination.limit" :total="total" :visible-pages="3"
                                    buttons-preset="primary" gapped />
                            </div>
                        </div>
                    </VaCardContent>
                </VaCard>
            </div>
        </div>
    </div>
    <RecordDeleteModal :project-id="projectId" :model-name="modelName" />
    <ChartCreationModal :project-id="projectId" :modelName="modelName" :fields="fields" :has-reference="!!refModel" />
    <RecordDetailsModal :reference-model="refModel" :fields="detailsFields" :id-fields="detailsIDFields" />
    <TSVExportModal :model-name="modelName" :project-id="projectId" :has-reference="!!refModel" />
    <TSVImportModal :model-name="modelName" :project-id="projectId" :ref-model="refModel" />

</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRecordStore } from '../stores/record-store';
import TSVExportModal from '../components/modals/TSVExportModal.vue';
import RecordDetailsModal from '../components/modals/RecordDetailsModal.vue';
import RecordDeleteModal from '../components/modals/RecordDeleteModal.vue';
import ChartCreationModal from '../components/modals/ChartCreationModal.vue';
import TSVImportModal from '../components/modals/TSVImportModal.vue';
import { useModelStore } from '../stores/model-store';
import { useProjectStore } from '../stores/project-store';
import RecordDataTable from '../components/tables/RecordDataTable.vue';

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()


const recordStore = useRecordStore()
const projectStore = useProjectStore()
const modelStore = useModelStore()
const editMode = ref(false)
const isArchived = computed(() => projectStore.isArchived)
const fields = computed(() => modelStore.filters)
const idFields = computed(() => modelStore.idFormat)
const refModel = computed(() => modelStore.refModel)

const total = computed(() => recordStore.total)

const detailsFields = computed(() => recordStore.isRefRecord ? refModel.value?.fields ?? [] : fields.value)
const detailsIDFields = computed(() => recordStore.isRefRecord ? refModel.value?.id_format ?? [] : idFields.value)

const offset = computed({
    get() {
        return recordStore.pagination.offset + 1
    }, set(v: number) {
        recordStore.pagination.offset = v - 1
    }
})

watch(() => props.modelName, async () => {
    await handleReset()
}, { immediate: true })


function toggleEditMode() {
    editMode.value = !editMode.value
}

async function handlePagination() {
    await recordStore.fetchRecords(props.projectId, props.modelName)
}

async function handleReset() {
    editMode.value = false
    recordStore.showRecordForm = false
    recordStore.resetForm()
    recordStore.resetSearchForm()
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.modelName)
}


</script>
<style scoped>
.mb-4 {
    margin-bottom: 1rem;
}
</style>