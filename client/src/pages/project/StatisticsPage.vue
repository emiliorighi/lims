<template>
    <div>
        <div style="min-height: 400px;" class="row align-center">
            <div v-for="ch, index in vaCharts" class="flex">
                <StatsCard :chart="ch" :index="index" @on-delete="deleteChart" :label="`${selected} of ${model}`" />
            </div>
            <div class="flex">
                <VaButton size="large" icon="add" @click="show = !show" />
            </div>
        </div>
        <VaModal v-model="show" title="Chart creation" hide-default-actions>
            <VaForm ref="chartForm">
                <VaSelect v-model="model" :options="['sample', 'experiment']" label="model"></VaSelect>
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
import { computed, onMounted, ref } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import { useSchemaStore } from '../../stores/schemas-store';
import StatsCard from './components/StatsCard.vue';
import { useForm } from 'vuestic-ui/web-components';


const { validate } = useForm('chartForm')
type ChartTypes = "line" | "bar" | "doughnut" | "pie" | "horizontal-bar"
type VaChartItem = {
    type: ChartTypes
    data: Record<string, number>
    model: 'sample' | 'experiment'
}
const schemaStore = useSchemaStore()
const model = ref<'sample' | 'experiment'>('sample')
const props = defineProps<{
    projectId: string
}>()

const show = ref(false)
const vaCharts = ref<VaChartItem[]>([])

const charts = ["line", "bar", "doughnut", "pie", "horizontal-bar"]

const chartType = ref<ChartTypes>('horizontal-bar')

const selected = ref('')

const fieldValues = computed(() => {
    if (!schemaStore.schema.project_id) return []
    return schemaStore.schema[model.value].fields.map(({ key }) => key)
})

onMounted(async () => {
    if (!schemaStore.schema.project_id) await getProject()
})

async function getProject() {
    try {
        const { data } = await ProjectService.getProject(props.projectId)
        schemaStore.schema = { ...data }
    } catch (error) {
        console.error(error)
    }
}

async function createChart() {

    if (!validate()) return

    try {
        const { data } = await ProjectService.getProjectStats(props.projectId, model.value, selected.value)
        vaCharts.value.push({
            data: data,
            type: chartType.value,
            model: model.value
        })
        show.value = !show.value
    } catch (err) {
        console.error(err)
    }
}

function deleteChart(index: number) {
    vaCharts.value.splice(index, 1)
}
</script>