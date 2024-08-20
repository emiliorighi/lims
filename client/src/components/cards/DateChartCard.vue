<template>
    <VaCard>
        <VaCardTitle>
            <h1 class="card-title text-tag text-secondary font-bold uppercase">{{ title }}</h1>
        </VaCardTitle>
        <VaCardContent>
            <div class="p-1 bg-black rounded absolute right-4 top-4">
                <VaIcon :name="icon" :color="color" size="large" />
            </div>
            <section>
                <div class="text-xl font-bold mb-2">{{ count }}</div>
            </section>
            <div class="w-full flex items-center">
                <VaChart :data="chartData" class="h-24" type="line" :options="options" />
            </div>
        </VaCardContent>
    </VaCard>
</template>

<script setup lang="ts">
import { VaCard } from 'vuestic-ui'
import VaChart from '../../components/va-charts/VaChart.vue'
import { TChartData } from '../../data/types'

const props = defineProps<{
    icon: string
    count: number
    title: string
    color: string
    chartData: TChartData
}>()

const options = {
    scales: {
        x: {
            display: false,
            grid: {
                display: false, // Disable X-axis grid lines ("net")
            },
        },
        y: {
            display: false,
            grid: {
                display: false, // Disable Y-axis grid lines ("net")
            },
            ticks: {
                display: false, // Hide Y-axis values
            },
        },
    },
    interaction: {
        intersect: false,
        mode: 'index',
    },
    plugins: {
        legend: {
            display: false,
        },
        tooltip: {
            enabled: true,
        },
    },
}
</script>