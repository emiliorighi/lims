<template>
    <VaModal max-height="500px" fixed-layout v-model="schemaStore.showReport" @ok="downloadData">
        <template #header>
            <h3 class="va-h3">
                Download Report
            </h3>
        </template>
        <VaInnerLoading :loading="isLoading">
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
import { Filter, ModelSearchForm } from '../../data/types'
import { AxiosError } from 'axios'
import { useToast } from 'vuestic-ui/web-components'
import ItemService from '../../services/clients/ItemService'

const { init } = useToast()
const isLoading = ref(false)


const props = defineProps<{
    searchForm: ModelSearchForm

}>()

const schemaStore = useSchemaStore()
const downloadFields = ref<string[]>([])
const applyFilters = ref(true)
const selectAllColumns = ref(false)

const mappedFields = computed(() => {
    return schemaStore.schema[schemaStore.model].fields.map((f: Filter) => { return { show: f.required, value: f.key } })
})

const options = computed(() => {
    return schemaStore.schema[schemaStore.model].fields.map(f => f.key)
})

async function downloadData() {
    let fields
    if (selectAllColumns.value) {
        fields = mappedFields.value.map(m => m.value)
    } else {
        fields = [...downloadFields.value]
    }
    const downloadRequest = { format: "tsv", fields: fields }
    try {
        isLoading.value = true
        const requestData = applyFilters.value ? {
            filter: props.searchForm.filter,
            sort_column: props.searchForm.sort_column, sort_order: props.searchForm.sort_order,
            ...props.searchForm.query,
            ...downloadRequest
        }
            :
            { ...downloadRequest }

        const response = await ItemService.getTsv(schemaStore.schema.project_id, schemaStore.model, requestData)
        const data = response.data
        const href = URL.createObjectURL(data);

        const filename = `${schemaStore.model}_report.tsv`
        // create "a" HTML element with href to file & click
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', filename); //or any other extension
        document.body.appendChild(link);
        link.click();
        // clean up "a" element & remove ObjectURL
        document.body.removeChild(link);
        URL.revokeObjectURL(href);

    } catch (e) {

        const axiosError = e as AxiosError
        init({ message: axiosError.message, color: 'danger' })

    } finally {
        isLoading.value = false
        schemaStore.showReport = false
    }
}
</script>