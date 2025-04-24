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
            <div v-for="model in mappedModels" class="flex flex-grow">
                <VaCard>
                    <VaCardContent>
                        <div class="row  align-center">
                            <div class="flex">
                                <div class="row align-center">
                                    <div class="flex">
                                        <VaIcon color="neutral" name="fa-cube" />
                                    </div>
                                    <div class="flex">
                                        <h2 class="va-h3">{{ model.name }}</h2>
                                    </div>
                                </div>
                            </div>
                            <div class="flex">
                                <VaChip color="backgroundElement" size="small" icon="fa-link" v-if="model.refModel">{{
                                    model.refModel }}
                                </VaChip>
                            </div>
                        </div>
                    </VaCardContent>
                    <VaCardContent>
                        <div class="row align-center justify-space-between">
                            <div class="flex">
                                <div class="row align-center">
                                    <div class="flex">
                                        <p class="va-text-secondary">Records:</p>
                                    </div>
                                    <div class="flex">
                                        <Counter :duration="1000" :target-value="model.counts" />
                                    </div>
                                </div>
                            </div>
                            <div class="flex">
                                <VaButton
                                    :to="{ name: 'records', params: { modelName: model.name, projectId: projectId } }"
                                    color="textPrimary" preset="secondary" icon="fa-arrow-up-right-from-square">View
                                </VaButton>
                            </div>
                        </div>
                    </VaCardContent>
                </VaCard>
            </div>
        </div>
        <div class="row row-equal">
            <div v-if="roots.length" class="flex flex-grow">
                <VaSkeleton variant="squared" v-if="projectStore.isLoading" />
                <VaCard>
                    <VaCardContent>
                        <div class="row justify-space-between align-center">
                            <div class="flex">
                                <h2 class="va-h4">Models relationship</h2>
                                <p class="va-text-secondary">
                                    Relationship between models and records
                                </p>
                            </div>
                        </div>
                    </VaCardContent>
                    <VaCardContent>
                        <HierachyChart :roots="roots" />
                    </VaCardContent>
                </VaCard>
            </div>
            <div v-for="chart in charts" class="flex flex-grow">
                <VaSkeleton variant="squared" v-if="projectStore.isLoading" />
                <ChartCard :key="chart.chartId" :chart="chart"></ChartCard>
            </div>
        </div>
        <!-- <div class="row">
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
        </div> -->
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
import Counter from '../components/ui/Counter.vue';
const props = defineProps<{
    projectId: string
}>()

const queryField = 'model_name'
const globalStore = useGlobalStore()
const projectStore = useProjectStore()

const mappedModels = computed(() => projectStore.mappedModels)
const roots = computed(() => transformToTree(mappedModels.value))
const recordStats = computed(() => globalStore.recordStats)
const charts = computed(() => {
    const charts = []
    // if (protocolStats.value.length) charts.push(createChart(Object.fromEntries(protocolStats.value), queryField, 'number of protocols by model', 'doughnut'))
    if (recordStats.value.length) charts.push(createChart(Object.fromEntries(recordStats.value), queryField, 'Records by model', 'doughnut', 'Number of records across the models'))
    // if (imagesStats.value.length) charts.push(createChart(Object.fromEntries(imagesStats.value), queryField, 'number of images by model', 'doughnut'))
    return charts
})

onMounted(async () => {
    await globalStore.lookupData()
    await projectStore.getProjectStats(props.projectId)
    await globalStore.getLinkStats(queryField, 'images', { project_id: props.projectId })
    await globalStore.getLinkStats(queryField, 'protocols', { project_id: props.projectId })
    await globalStore.getRecordStats(queryField, { project_id: props.projectId })
});

function transformToTree(models: { name: string, refModel?: string, counts: number }[]) {
    const nodes: Record<string, any> = {};
    const childrenSet = new Set<string>();

    // Step 1: Create all nodes
    models.forEach(m => {
        nodes[m.name] = {
            name: m.name,
            children: [],
            value: m.counts,
        };
    });

    // Step 2: Link children and record child names
    models.forEach(m => {
        if (m.refModel && nodes[m.refModel]) {
            nodes[m.refModel].children.push(nodes[m.name]);
            childrenSet.add(m.name);
        }
    });

    // Step 3: Only nodes not in childrenSet are roots
    const roots = models
        .filter(m => !childrenSet.has(m.name))
        .map(m => nodes[m.name]);

    return roots;
}




function createChart(frequencies: Record<string, number>, fieldKey: string, label: string, type: ChartTypes, description?: string) {

    const data = processChartData(frequencies, fieldKey);
    const chartOptions = getChartOptions(type);
    return {
        chartId: label,
        chartOptions,
        type: type,
        data,
        label,
        description
    }
}


</script>