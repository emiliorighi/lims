<template>
    <VaModal max-height="400px" fixed-layout v-model="experimentStore.showReport" hide-default-actions>
        <template #header>
            <h3 class="va-h3">
                Download Report
            </h3>
        </template>
        <VaInnerLoading :loading="isLoading">
            <div class="row">
                <VaSelect class="flex lg12 md12 sm12 xs12" v-model="downloadFields"
                    searchPlaceholderText="Type to search" label="Columns"
                    :options="schemaStore.schema.experiment.fields.map(f => f.key)" placeholder="Column list" multiple
                    :messages="['Search fields to use as TSV columns']" />
            </div>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCheckbox style="margin-top: 6px;" v-model="applyFilters" label="Apply current filter">
                    </VaCheckbox>
                    <VaCheckbox style="margin-top: 6px;" v-model="selectAllColumns" label="Select all columns">
                    </VaCheckbox>
                </div>
            </div>
        </VaInnerLoading>
        <template #footer>
            <VaButton @click="downloadData"> Submit</VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useSchemaStore } from '../../../stores/schemas-store'
import { Filter } from '../../../data/types'
import { AxiosError } from 'axios'
import { useToast } from 'vuestic-ui/web-components'
import ExperimentService from '../../../services/clients/ExperimentService'
import { useExperimentStore } from '../../../stores/experiment-store'

const { init } = useToast()
const isLoading = ref(false)

const experimentStore = useExperimentStore()
const schemaStore = useSchemaStore()
const downloadFields = ref<string[]>([])
const applyFilters = ref(true)
const selectAllColumns = ref(false)

const mappedFields = schemaStore.schema.experiment.fields.map((f: Filter) => { return { show: f.required, value: f.key } }
)


async function downloadData() {
    let fields
    if (selectAllColumns.value) {
        fields = mappedFields.map(m => m.value)
    } else {
        fields = [...downloadFields.value]
    }
    const downloadRequest = { format: "tsv", fields: fields }
    try {
        isLoading.value = true
        const requestData = applyFilters.value ? {
            filter: experimentStore.searchForm.filter,
            sort_column: experimentStore.searchForm.sort_column, sort_order: experimentStore.searchForm.sort_order,
            ...experimentStore.searchForm.query,
            ...downloadRequest
        }
            :
            { ...downloadRequest }

        const response = await ExperimentService.getTsv(schemaStore.schema.project_id, requestData)
        const data = response.data
        const href = URL.createObjectURL(data);

        const filename = 'experiment_report.tsv'
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
        console.error(e)
        const axiosError = e as AxiosError
        init({ message: axiosError.message, color: 'danger' })

    } finally {
        isLoading.value = false
    }
}
</script>