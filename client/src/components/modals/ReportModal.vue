<template>
    <VaModal max-height="500px" hide-default-actions fixed-layout v-model="itemStore.showReport">
        <template #header>
            <Header title="Download Report" :icon="icon" />
        </template>
        <VaInnerLoading :loading="itemStore.isTSVLoading">
            <div class="row">
                <VaSelect class="flex lg12 md12 sm12 xs12" v-model="downloadFields"
                    searchPlaceholderText="Type to search" label="Columns" :options="options" placeholder="Column list"
                    multiple :messages="['Search fields to use as TSV columns']" />
            </div>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCheckbox style="margin-top: 6px;" v-model="applyFilters" label="Apply current filters">
                    </VaCheckbox>
                    <VaCheckbox style="margin-top: 6px;margin-left: 3px;" v-model="selectAllColumns"
                        label="Select all columns">
                    </VaCheckbox>
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
import { useSchemaStore } from '../../stores/schema-store'
import { useItemStore } from '../../stores/item-store'
import Header from './common/Header.vue'

const props = defineProps<{
    icon: string
}>()

const itemStore = useItemStore()
const schemaStore = useSchemaStore()

const downloadFields = ref<string[]>([])
const applyFilters = ref(true)
const selectAllColumns = ref(false)
const model = computed(() => itemStore.currentModel)

const options = computed(() => {
    return schemaStore.schema[model.value].fields.map(f => f.key)
})

watch(() => selectAllColumns.value, () => {
    if (selectAllColumns.value) downloadFields.value = [...options.value]
})

async function downloadData() {
    const { project_id } = schemaStore.schema
    await itemStore.downloadData(project_id, downloadFields.value, applyFilters.value)
}
</script>