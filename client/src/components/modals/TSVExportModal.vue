<template>
    <VaModal closeable hide-default-actions fixed-layout v-model="recordStore.showReportModal">
        <template #header>
            <div class="row align-center justify-space-between">
                <div class="flex">
                    <h3 class="va-h3">
                        Export Records
                    </h3>
                    <p class="va-text-secondary">Export records in a TSV file</p>
                </div>
                <VaIcon color="textPrimary" size="large" class="flex" name="fa-file-export" />
            </div>
        </template>
        <VaInnerLoading :loading="recordStore.isTSVLoading">
            <div class="layout fluid va-gutter-5">
                <div class="row">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaSelect v-model="downloadFields" searchPlaceholderText="Type to search" label="Columns"
                            :options="options" placeholder="Column list" multiple
                            :messages="['Search fields to use as TSV columns']" />
                    </div>
                    <div class="flex lg6 md6 sm12 xs12">
                        <VaCheckbox v-model="applyFilters" label="Apply current filters">
                        </VaCheckbox>
                    </div>
                    <div class="flex lg6 md6 sm12 xs12">
                        <VaCheckbox v-model="selectAllColumns" label="Select all columns">
                        </VaCheckbox>
                    </div>
                </div>
            </div>
        </VaInnerLoading>
        <template #footer>
            <VaButton @click="downloadData"> Submit </VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRecordStore } from '../../stores/record-store';
import { ResearchModel } from '../../data/types';
import { useModelStore } from '../../stores/model-store';

const props = defineProps<{
    projectId: string,
    modelName: string
}>()

const recordStore = useRecordStore()
const modelStore = useModelStore()
const downloadFields = ref<string[]>([])
const applyFilters = ref(true)
const selectAllColumns = ref(false)

const options = computed(() => modelStore.filters.map(({ key }) => key) ?? [])

watch(() => selectAllColumns.value, () => {
    if (selectAllColumns.value) downloadFields.value = [...options.value]
    else downloadFields.value = []
})

async function downloadData() {
    await recordStore.downloadData(props.projectId, props.modelName, downloadFields.value, applyFilters.value)
}
</script>