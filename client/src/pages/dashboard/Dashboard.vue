<template>
    <div>
        <h1 class="va-h1">Dashboard</h1>
        <div class="row row-equal">
            <div v-if="chartData" class="flex lg8 md8 sm12 xs12">
                <VaCard>
                    <VaCardTitle class="va-text-secondary">
                        Data contained in each project
                    </VaCardTitle>
                    <VaCardContent style="height: 400px;">
                        <VaChart type="horizontal-bar" :data="chartData" />
                    </VaCardContent>
                </VaCard>
            </div>
            <div class="flex lg4 md4 sm12 xs12">
                <div class="row row-equal">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaCard>
                            <VaCardContent>
                                <div class="row justify-space-between align-center">
                                    <div class="flex">
                                        <h4 class="va-h4">
                                            {{ allData.projects }}
                                        </h4>
                                        <p>Projects</p>
                                    </div>
                                    <div class="flex">
                                        <VaIcon color="info" name="folder" size="large"></VaIcon>
                                    </div>
                                </div>
                            </VaCardContent>
                        </VaCard>
                    </div>
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaCard>
                            <VaCardContent>
                                <div class="row justify-space-between align-center">
                                    <div class="flex">
                                        <h4 class="va-h4">
                                            {{ allData.samples }}
                                        </h4>
                                        <p>Samples</p>
                                    </div>
                                    <div class="flex">
                                        <VaIcon color="success" name="fa-vial" size="large"></VaIcon>
                                    </div>
                                </div>
                            </VaCardContent>
                        </VaCard>
                    </div>
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaCard>
                            <VaCardContent>
                                <div class="row justify-space-between align-center">
                                    <div class="flex">
                                        <h4 class="va-h4">
                                            {{ allData.experiments }}
                                        </h4>
                                        <p>Experiments</p>
                                    </div>
                                    <div class="flex">
                                        <VaIcon color="primary" name="fa-dna" size="large"></VaIcon>
                                    </div>
                                </div>
                            </VaCardContent>
                        </VaCard>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import StatsService from '../../services/clients/StatsService'
import VaChart from '../../components/va-charts/VaChart.vue'
import { TChartData } from '../../data/types'
import ProjectService from '../../services/clients/ProjectService'
import SampleService from '../../services/clients/SampleService'
import ExperimentService from '../../services/clients/ExperimentService'

const chartData = ref<TChartData>()

const allData = reactive<{
    samples: number,
    experiments: number,
    projects: number
}>({
    samples: 0,
    experiments: 0,
    projects: 0
})
onMounted(async () => {
    try {
        const sampleData = await getStats('samples')
        const experimentData = await getStats('experiments')
        chartData.value = createChartData(sampleData, experimentData)
        const projectResp = await ProjectService.getProjects({})
        const sampleResp = await SampleService.getAllSamples({})
        const expResp = await ExperimentService.getAllExperiments({})
        allData.projects = projectResp.data.total
        allData.samples = sampleResp.data.total
        allData.experiments = expResp.data.total
    } catch (err) {
        console.log(err)
    }

})

const colors = ['#2c82e0', '#ef476f', '#ffd166', '#06d6a0', '#8338ec', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#c9cbcf', '#e74c3c', '#3498db', '#2ecc71', '#f1c40f',
    '#e67e22', '#1abc9c', '#9b59b6', '#34495e', '#95a5a6', '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#f39c12',
    '#d35400', '#2c3e50', '#bdc3c7', '#7f8c8d', '#e74c3c', '#2980b9', '#f1c40f', '#2ecc71', '#9b59b6'
]

async function getStats(model: 'samples' | 'experiments') {
    try {
        const { data } = await StatsService.getStats(model, 'project')
        return data
    } catch (err) {
        console.error(err)
    }
}

function createChartData(sampleData: Record<string, number>, experimentData: Record<string, number>) {
    const sampleEntries = Object.entries(sampleData)
    const experimentEntries = Object.entries(experimentData)
    const uniqueLabels = Array.from(new Set([...sampleEntries.map(([k, v]) => k), ...experimentEntries.map(([k, v]) => k)]));

    const orderedSampleEntries = uniqueLabels.map(l => {
        const p = sampleEntries.find(([k, v]) => k === l)
        if (p) return [l, p[1]]
        return [l, 0]
    })
    const orderedExperimentEntries = uniqueLabels.map(l => {
        const p = experimentEntries.find(([k, v]) => k === l)
        if (p) return p
        return [l, 0]
    })

    return {
        labels: uniqueLabels,
        datasets: [
            {
                backgroundColor: '#2c82e0',
                label: 'Samples',
                data: orderedSampleEntries.map(([k, v]) => v),
            },
            {
                backgroundColor: '#ef476f',
                label: 'Experiments',
                data: orderedExperimentEntries.map(([k, v]) => v),
            }
        ]
    }
}


</script>