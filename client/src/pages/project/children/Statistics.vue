<template>
    <VaModal max-height="" :fixed-layout="false" size="large" v-model="schemaStore.showChart" hide-default-actions>
        <template #header>
            <h3 class="va-h3">Chart creation</h3>
        </template>
        <div class="row align-end">
            <div class="flex lg6 md6 sm12 xs12 p-6">
                <VaSelect :disabled="modelOptions.length === 1" v-model="model" :options="modelOptions" label="model">
                </VaSelect>
            </div>
            <div class="flex lg6 md6 sm12 xs12 p-6">
                <VaSelect v-model="chartType" :options="charts" label="chart type"></VaSelect>
            </div>
            <div class="flex lg6 md6 sm12 xs12 p-6">
                <VaSelect :rules="[(v: string) => !!v || 'Field is mandatory']" v-model="selected"
                    :options="fieldValues" label="field"></VaSelect>
            </div>
        </div>
        <VaDivider />
        <div class="row">
            <div v-for="ch, index in vaCharts" class="flex lg12 md12 sm12 xs12">
                <StatsCard :chart="ch" :index="index" @on-delete="deleteChart" :label="`${ch.model}s by ${ch.field} `"
                    :chartId="`${ch.field}_${ch.model}_${ch.type}`" />
            </div>
        </div>
        <template #footer>
            <VaButton :disabled="!chartType || !selected" @click="createChart">Create Chart</VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useSchemaStore } from '../../../stores/schemas-store';
import StatsCard from '../../../components/cards/StatsCard.vue';
import { VaChartItem, ChartTypes, ColumnSizes } from '../../../data/types'
import ItemService from '../../../services/clients/ItemService';

const schemaStore = useSchemaStore()
const model = ref<'sample' | 'experiment'>('sample')

const modelOptions = computed(() => {
    if (schemaStore.schema.experiment.id_format.length) return ['sample', 'experiment']
    return ['sample']
})

const show = ref(false)
const vaCharts = ref<VaChartItem[]>([])

const charts = ["line", "bar", "doughnut", "pie", "horizontal-bar"]

const chartType = ref<ChartTypes>('horizontal-bar')
const size = ref<ColumnSizes>('1')
const selected = ref('')

const fieldValues = computed(() => {
    if (!schemaStore.schema.project_id) return []
    return schemaStore.schema[model.value].fields.map(({ key }) => key)
})

async function createChart() {
    const type = chartType.value
    const m = model.value
    const s = size.value

    try {
        const { data } = await ItemService.getStats(schemaStore.schema.project_id, model.value, selected.value)
        const ch =
        {
            data: data,
            type,
            model: m,
            field: selected.value,
            size: s
        }
        vaCharts.value.unshift({ ...ch })
        show.value = !show.value
    } catch (err) {
        console.error(err)
    }
}

function deleteChart(index: number) {
    vaCharts.value.splice(index, 1)
}


</script>