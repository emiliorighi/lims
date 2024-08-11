<template>
    <VaCard>
        <VaCardTitle>
            <div class="row justify-space-between">
                <div class="flex p-0">{{ label }}</div>
                <div class="flex p-0 a-text-secondary">
                    <VaButton size="small" @click="emits('onDelete', index)" icon="delete" color="danger" />
                </div>
            </div>
        </VaCardTitle>
        <VaCardContent>
            <VaChart :type="chart.type" :data="createChartData(chart.data)" />
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import VaChart from '../va-charts/VaChart.vue';

const emits = defineEmits(['onDelete'])
type ChartTypes = "line" | "bar" | "bubble" | "doughnut" | "pie" | "horizontal-bar"

const props = defineProps<{
    chart: {
        type: ChartTypes
        data: Record<string, number>
    }
    index: number,
    label: string
}>()

const colors = ['#2c82e0', '#ef476f', '#ffd166', '#06d6a0', '#8338ec', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#c9cbcf', '#e74c3c', '#3498db', '#2ecc71', '#f1c40f',
    '#e67e22', '#1abc9c', '#9b59b6', '#34495e', '#95a5a6', '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#f39c12',
    '#d35400', '#2c3e50', '#bdc3c7', '#7f8c8d', '#e74c3c', '#2980b9', '#f1c40f', '#2ecc71', '#9b59b6'
]

function createChartData(data: Record<string, number>) {
    const entries = Object.entries(data)

    const labels = entries.map(([k, v]) => k)

    return {
        labels: labels,
        datasets: [
            {
                backgroundColor: colors,
                label: props.label,
                data: Object.values(data),
            },
        ],
    }
}


</script>