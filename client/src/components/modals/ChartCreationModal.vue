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
                    <VaButton block :disabled="!chartType || !selectedField" @click="createChart">
                        Create
                        Chart
                    </VaButton>
                </div>
            </div>
        </div>
        <div v-for="chart in charts" :key="chart.chartId" class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <ChartCard :chart="chart" />
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { ChartItem, ChartTypes, InputType, ResearchFilter } from '../../data/types'
import { useRecordStore } from '../../stores/record-store';
import { useDateChart, processChartData, getChartOptions } from '../../composables/chartConfigs';
import { useColors } from 'vuestic-ui/web-components';
import ChartCard from '../cards/ChartCard.vue';

const props = defineProps<{
    modelName: string,
    fields: ResearchFilter[]
    projectId: string,
    hasReference: boolean
}>()

const colors = useColors()

const fields = computed(() => {
    const fields = props.fields.map(({ key, type }) => ({ key, type }))
    if (props.hasReference) fields.push({ key: 'reference_id', type: 'select' })
    return fields
})

const selectedField = ref<{ key: string, type: InputType } | null>(null)

const chartTypes = ["line", "doughnut", "pie", "horizontal-bar"]

const recordStore = useRecordStore()
const applyFilters = ref(true)
const chartType = ref<ChartTypes | null>(null)
const charts = ref<ChartItem[]>([])
const chartId = computed(() => `${selectedField.value?.key}_${chartType}`)
const label = computed(() => `${props.modelName} by ${selectedField.value?.key} `)

watch(() => recordStore.showChartModal, () => reset())

function reset() {
    chartType.value = null
    charts.value = []
    selectedField.value = null
}

async function createChart() {
    if (!selectedField.value || !chartType.value) return;

    const fieldKey = selectedField.value.key;
    const isDate = selectedField.value.type === 'date';
    const frequencies = await recordStore.getFieldFrequencies(
        props.projectId,
        props.modelName,
        fieldKey,
        !applyFilters.value
    );

    let data, chartOptions;

    if (isDate) {
        const result = useDateChart(frequencies, fieldKey, colors.getColor('primary'));
        data = {
            labels: result.labels,
            datasets: result.datasets
        };
        chartOptions = result.options;
    } else {
        data = processChartData(frequencies, fieldKey);
        chartOptions = getChartOptions(chartType.value);
    }

    charts.value = [{
        chartId: chartId.value,
        chartOptions,
        type: chartType.value,
        data,
        label: label.value
    }];
}


</script>