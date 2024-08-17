<template>
    <VaModal max-height="500px" fixed-layout v-model="itemStore.showReport" @ok="downloadData">
        <template #header>
            <Header title="Download Report" :icon="icon" />
        </template>
        <VaInnerLoading :loading="itemStore.isLoading">
            <div class="row">
                <VaSelect class="flex lg12 md12 sm12 xs12" v-model="downloadFields"
                    searchPlaceholderText="Type to search" label="Columns" :options="options" placeholder="Column list"
                    multiple :messages="['Search fields to use as TSV columns']" />
            </div>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCheckbox style="margin-top: 6px;" v-model="applyFilters" label="Apply current filters">
                    </VaCheckbox>
                    <VaCheckbox style="margin-top: 6px;" v-model="selectAllColumns" label="Select all columns">
                    </VaCheckbox>
                </div>
            </div>
        </VaInnerLoading>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useSchemaStore } from './../../stores/schemas-store'
import { Filter, ModelType } from '../../data/types'
import { useItemStore } from '../../stores/item-store'
import Header from './common/Header.vue'

const props = defineProps<{
    icon: string
    model: ModelType
}>()

const itemStore = useItemStore()
const schemaStore = useSchemaStore()

const downloadFields = ref<string[]>([])
const applyFilters = ref(true)
const selectAllColumns = ref(false)

const mappedFields = computed(() => {
    return schemaStore.schema[props.model].fields.map((f: Filter) => { return { show: f.required, value: f.key } })
})
const options = computed(() => {
    return schemaStore.schema[props.model].fields.map(f => f.key)
})

async function downloadData() {
    let fields
    if (selectAllColumns.value) {
        fields = mappedFields.value.map(m => m.value)
    } else {
        fields = [...downloadFields.value]
    }
    const downloadRequest = { format: "tsv", fields: fields }
    const requestData = applyFilters.value ? {
        filter: itemStore.searchForm.filter,
        sort_column: itemStore.searchForm.sort_column, sort_order: itemStore.searchForm.sort_order,
        ...itemStore.searchForm.query,
        ...downloadRequest
    }
        :
        { ...downloadRequest }

    await itemStore.downloadData(requestData, schemaStore.schema.project_id, props.model)
}
</script>