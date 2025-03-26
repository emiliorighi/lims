<template>
    <VaModal size="large" v-model="recordStore.showChartModal" hide-default-actions close-button>
        <template #header>
            <h3 class="va-h3">Chart creation</h3>
            <p class="va-text-secondary">Fill the form to create and download a chart</p>
        </template>
        <div class="layout va-gutter-5 fluid">
            <div class="row align-end">
                <div class="flex lg6 md6 sm12 xs12">
                    <VaSelect text-by="key" v-model="selectedField" :options="fields" label="Target field">
                    </VaSelect>
                </div>
                <div class="flex lg6 md6 sm12 xs12">
                    <VaSelect v-model="chartType" :options="chartTypes" label="Chart type"></VaSelect>
                </div>
                <div class="flex lg6 md6 sm12 xs12">
                    <VaCheckbox label="Apply current filters" v-model="applyFilters" />
                </div>
                <div class="flex lg12 md12 sm12 xs12">
                    <VaButton :disabled="!chartType || !selectedField" @click="createChart">Create Chart</VaButton>
                </div>
            </div>
        </div>
        <VaDivider />
        <div v-if="chartData.labels && chartData.datasets && chartOptions && chartType" class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <StatsCard :type="chartType" :chart-options="chartOptions" :data="chartData"
                    :label="`${model.name}s by ${selectedField?.key} `"
                    :chartId="`${selectedField?.key}_${chartType}`" />
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useSchemaStore } from '../../../stores/schema-store';
import StatsCard from '../../../components/cards/StatsCard.vue';
import { ChartTypes, ReseachModel, InputType } from '../../../data/types'
import { useRecordStore } from '../../../stores/record-store';
import { useDateChart, processChartData, getChartOptions } from '../../../composables/chartConfigs';
import { useColors } from 'vuestic-ui/web-components';


const props = defineProps<{
    model: ReseachModel
    projectId: string
}>()

const colors = useColors()

const fields = computed(() => props.model.fields.map(({ key, type }) => ({ key, type })))
const selectedField = ref<{ key: string, type: InputType } | null>(null)

const chartTypes = ["line", "bar", "doughnut", "pie", "horizontal-bar"]

const schemaStore = useSchemaStore()
const recordStore = useRecordStore()
const applyFilters = ref(true)
const chartType = ref<ChartTypes | null>(null)
const chartData = ref<{ datasets: any, labels: any }>({
    datasets: null,
    labels: null
})

const chartOptions = ref()

async function createChart() {
    if (!selectedField.value || !chartType.value) return
    resetChart()
    const frequencies = await recordStore.getFieldFrequencies(props.projectId, props.model.name, selectedField.value?.key, !applyFilters.value)
    if (selectedField.value.type === 'date') {
        const { datasets, labels, options } = useDateChart(frequencies, selectedField.value.key, colors.getColor('primary'))
        chartOptions.value = { ...options }
        chartData.value.datasets = datasets
        chartData.value.labels = labels
        return
    }
    chartData.value = processChartData(frequencies, selectedField.value.key)
    chartOptions.value = getChartOptions(chartType.value)

}


function resetChart() {
    chartOptions.value = null
    chartData.value = { datasets: null, labels: null }
}
</script>