<template>
    <div>
        <div style="min-height: 400px;" class="row align-center">
            <div v-for="ch, index in vaCharts" class="flex">
                <StatsCard :chart="ch" :index="index" @on-delete="deleteChart" :label="`${ch.field} field of ${ch.model}`" />
            </div>
            <div class="flex">
                <VaButton size="large" icon="add" @click="show = !show" />
            </div>
        </div>
        <VaModal v-model="show" hide-default-actions>
            <template #header>
                <h3 class="va-h3">Chart creation</h3>
            </template>
            <VaForm ref="chartForm">
                <VaSelect :disabled="modelOptions.length === 1" v-model="model" :options="modelOptions" label="model">
                </VaSelect>
                <VaSelect v-model="chartType" :options="charts" label="chart type"></VaSelect>
                <VaSelect :rules="[(v: string) => !!v || 'Field is mandatory']" v-model="selected"
                    :options="fieldValues" label="field"></VaSelect>
            </VaForm>
            <template #footer>
                <VaButton @click="createChart">Create Chart</VaButton>
            </template>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import { useSchemaStore } from '../../stores/schemas-store';
import StatsCard from './components/StatsCard.vue';
import { useForm } from 'vuestic-ui/web-components';


const { validate } = useForm('chartForm')
type ChartTypes = "line" | "bar" | "doughnut" | "pie" | "horizontal-bar"
type VaChartItem = {
    type: ChartTypes
    data: Record<string, number>
    model: 'sample' | 'experiment',
    field: string
}
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

const selected = ref('')

const fieldValues = computed(() => {
    if (!schemaStore.schema.project_id) return []
    return schemaStore.schema[model.value].fields.map(({ key }) => key)
})



async function createChart() {

    if (!validate()) return
    const type = chartType.value
    const m = model.value

    try {
        const { data } = await ProjectService.getProjectStats(schemaStore.schema.project_id, model.value, selected.value)
        const ch =
        {
            data: data,
            type,
            model: m,
            field: selected.value
        }
        vaCharts.value.push({ ...ch })
        show.value = !show.value
    } catch (err) {
        console.error(err)
    }
}

function deleteChart(index: number) {
    vaCharts.value.splice(index, 1)
}
</script>