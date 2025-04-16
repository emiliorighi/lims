<template>
    <div>
        <div class="row justify-space-between align-end">
            <div class="flex">
                <h1 class="va-h1">Project Dashboard</h1>
                <p class="va-text-secondary">
                    Details and stats of {{ projectId }}
                </p>
            </div>
        </div>
        <div class="row">
            <div class="flex lg8 md6 sm12 xs12">
                <ProjectDetailsCard v-if="projectStore.schema" :project="projectStore.schema" />
                <VaSkeleton variant="squared" v-else />
            </div>
            <div class="flex lg4 md6 sm12 xs12">
                <div v-if="roots.length" class="row">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaSkeleton variant="squared" v-if="projectStore.isLoading" />
                        <VaCard>
                            <VaCardActions align="between">
                                <h2 class="va-h6">Models Relationship</h2>
                            </VaCardActions>
                            <HierachyChart :roots="roots" />
                        </VaCard>
                    </div>
                </div>
                <div class="row row-equal">
                    <div v-for="chart in charts" class="flex lg12 md12 sm12 xs12">
                        <VaSkeleton variant="squared" v-if="projectStore.isLoading" />
                        <ChartCard :key="chart.chartId" :chart="chart"></ChartCard>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import HierachyChart from '../components/charts/HierachyChart.vue';
import { useProjectStore } from '../stores/project-store';
import { useGlobalStore } from '../stores/global-store';
import { getChartOptions, processChartData } from '../composables/chartConfigs';
import { ChartTypes } from '../data/types';
import ChartCard from '../components/cards/ChartCard.vue';
import ProjectDetailsCard from '../components/cards/ProjectDetailsCard.vue';

const props = defineProps<{
    projectId: string
}>()

const queryField = 'model_name'
const globalStore = useGlobalStore()
const projectStore = useProjectStore()

const roots = computed(() => transformToTree(projectStore.mappedModels))
const recordStats = computed(() => globalStore.recordStats)
const protocolStats = computed(() => globalStore.protocolStats)
const imagesStats = computed(() => globalStore.imageStats)
const charts = computed(() => {
    const charts = []
    if (protocolStats.value.length) charts.push(createChart(Object.fromEntries(protocolStats.value), queryField, 'number of protocols by model', 'doughnut'))
    if (recordStats.value.length) charts.push(createChart(Object.fromEntries(recordStats.value), queryField, 'number of records by model', 'doughnut'))
    if (imagesStats.value.length) charts.push(createChart(Object.fromEntries(imagesStats.value), queryField, 'number of images by model', 'doughnut'))
    return charts
})

onMounted(async () => {
    await globalStore.lookupData()
    await projectStore.getProjectStats(props.projectId)
    await globalStore.getLinkStats(queryField, 'images', { project_id: props.projectId })
    await globalStore.getLinkStats(queryField, 'protocols', { project_id: props.projectId })
    await globalStore.getRecordStats(queryField, { project_id: props.projectId })
});

function transformToTree(models: { name: string, refModel: string | undefined, counts: number }[]) {
    const nodes: Record<string, any> = {};

    models.forEach(m => {
        nodes[m.name] = {
            name: m.name,
            children: [],
            value: m.counts,
        };
    });

    models.forEach((m) => {
        if (m.refModel && nodes[m.refModel]) {
            nodes[m.refModel].children.push(nodes[m.name]);
        }
    });
    // Find root nodes (not referenced by any model)
    const referenced = new Set(models.map(m => m.refModel).filter(Boolean));
    const roots = models.filter((m: any) => referenced.has(m.name)).map((m: any) => nodes[m.name]);
    return roots
    //   return {
    //     name: 'Models Relationship',
    //     children: roots
    //   };
}



function createChart(frequencies: Record<string, number>, fieldKey: string, label: string, type: ChartTypes) {

    const data = processChartData(frequencies, fieldKey);
    const chartOptions = getChartOptions(type);
    return {
        chartId: label,
        chartOptions,
        type: type,
        data,
        label
    }
}


</script>