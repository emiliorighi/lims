<template>
    <div>
        <div class="row justify-space-between align-end">
            <h1 class="va-h1 flex pt-0 mb-0">Dashboard</h1>
        </div>
        <div class="row row-equal">
            <div class="flex lg8 md8 sm12 xs12">
                <VaCard v-if="expData && sampleData">
                    <!-- <VaCardTitle class="va-text-secondary">
                        Data contained in each project
                    </VaCardTitle> -->
                    <VaCardContent style="height: 400px;">
                        <VaChart :options="chartOptions" type="horizontal-bar"
                            :data="createChartData(sampleData, expData)" />
                    </VaCardContent>
                </VaCard>
                <VaSkeleton v-else height="400px" />
            </div>
            <div class="flex lg4 md4 sm12 xs12 cards-column">
                <div v-for="(card, index) in Object.values(cards)" :key="index" class="row row-equal card-wrapper">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaCard class="card">
                            <VaCardContent>
                                <div class="row justify-space-between align-center">
                                    <div class="flex">
                                        <Counter :duration="2000" :target-value="card.count" />
                                        <p>
                                            {{ card.text }}
                                        </p>
                                    </div>
                                    <div class="flex">
                                        <VaIcon :color="card.color" :name="card.icon" size="large"></VaIcon>
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
import { onMounted, ref } from 'vue'
import StatsService from '../../services/clients/StatsService'
import VaChart from '../../components/va-charts/VaChart.vue'
import { DashboardCard } from '../../data/types'
import ProjectService from '../../services/clients/ProjectService'
import ItemService from '../../services/clients/ItemService'
import { AxiosResponse } from 'axios'
import Counter from '../../components/ui/Counter.vue'

const expData = ref<Record<string, number> | undefined>()
const sampleData = ref<Record<string, number> | undefined>()
const cards = ref<{
    samples: DashboardCard,
    experiments: DashboardCard,
    projects: DashboardCard
}>({
    samples: {
        icon: 'fa-vial',
        text: 'Samples',
        color: 'success',
        count: 0
    },
    experiments: {
        icon: 'fa-dna',
        text: 'Experiments',
        color: 'primary',
        count: 0
    },
    projects: {
        icon: 'folder',
        text: 'Projects',
        color: 'secondary',
        count: 0
    }
})
const chartOptions = {
    plugins: {
        title: {
            text: 'Number of Samples and Experiments by Project',
            display: true,
            align: 'start'
        },
        datalabels: {
            color: '#ffffff',
            font: {
                size: '18'
            }
        },
        legend: { position: 'bottom', align: 'center' }
    },

}
onMounted(async () => {
    try {

        // Get stats and create chart
        sampleData.value = { ...await getStats('samples') }
        expData.value = { ...await getStats('experiments') }
        // Get object count
        cards.value.projects.count = getTotal(await ProjectService.getProjects({}))
        cards.value.samples.count = getTotal(await ItemService.getAllItems('sample', {}))
        cards.value.experiments.count = getTotal(await ItemService.getAllItems('experiment', {}))
    } catch (err) {
        console.log(err)
    }

})

function getTotal(response: AxiosResponse) {
    const { data } = response as Record<string, any>
    const { total } = data
    return total

}

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
<style scoped>
.cards-column {
    display: flex;
    flex-direction: column;
}

.card-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.card {
    flex: 1;
    display: flex;
    flex-direction: column;
}
</style>