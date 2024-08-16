<template>
    <Header :title="title" />

    <div class="row justify-space-between align-center">
        <div class="flex p-0">
            <h4 class="va-h4">Statistics</h4>
            <p class="va-text-secondary mb-4">Create and save customized charts</p>
        </div>
        <div class="flex">
            <VaButton icon="add" @click="show = !show"> Chart</VaButton>
        </div>
    </div>
    <div>
        <div class="row row-equal align-center">
            <div v-for="ch, index in vaCharts" :class="mapSize(ch.size)">
                <StatsCard :chart="ch" :index="index" @on-delete="deleteChart" :label="`${ch.model}s by ${ch.field} `"
                    :chartId="`${ch.field}_${ch.model}_${ch.type}`" />
            </div>
        </div>
        <VaModal v-model="show" hide-default-actions>
            <template #header>
                <h3 class="va-h3">Chart creation</h3>
            </template>
            <VaForm ref="chartForm">
                <div class="row align-end">
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaSelect :disabled="modelOptions.length === 1" v-model="model" :options="modelOptions"
                            label="model">
                        </VaSelect>
                    </div>
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaSelect v-model="chartType" :options="charts" label="chart type"></VaSelect>
                    </div>
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaSelect v-model="size" :options="['1', '2', '3', '4']" label="chart size"></VaSelect>
                    </div>
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaSelect :rules="[(v: string) => !!v || 'Field is mandatory']" v-model="selected"
                            :options="fieldValues" label="field"></VaSelect>
                    </div>
                </div>
            </VaForm>
            <template #footer>
                <VaButton @click="createChart">Create Chart</VaButton>
            </template>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import ProjectService from '../../../services/clients/ProjectService';
import { useSchemaStore } from '../../../stores/schemas-store';
import StatsCard from '../../../components/cards/StatsCard.vue';
import { useForm } from 'vuestic-ui/web-components';
import { VaChartItem, ChartTypes, ColumnSizes } from '../../../data/types'
import Header from '../../../components/ui/Header.vue'

const props = defineProps<{
    title: string
}>()
const { validate } = useForm('chartForm')

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

    if (!validate()) return
    const type = chartType.value
    const m = model.value
    const s = size.value

    try {
        const { data } = await ProjectService.getProjectStats(schemaStore.schema.project_id, model.value, selected.value)
        const ch =
        {
            data: data,
            type,
            model: m,
            field: selected.value,
            size: s
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

function mapSize(size: ColumnSizes) {
    switch (size) {
        case '1':
            return 'flex lg3 md3 sm12 xs12'
        case '2':
            return 'flex lg6 md6 sm12 xs12'
        case '3':
            return 'flex lg9 md9 sm12 xs12'
        case '4':
            return 'flex lg12 md12 sm12 xs12'
    }
}

</script>