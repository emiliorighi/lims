<template>
    <VaCard color="background-element">
        <VaCardActions align="between">
            <VaButton preset="primary" @click="downloadCanvasAsPNG(chartId, `${chartId}.png`)">Download</VaButton>
            <VaButton preset="primary" @click="emits('onDelete', index)" color="danger">
                Delete
            </VaButton>
        </VaCardActions>
        <VaCardContent style="height: 400px;">

            <VaChart :chart-id="chartId" :type="chart.type" :options="chartOptions"
                :data="createChartData(chart.data)" />
        </VaCardContent>

    </VaCard>
</template>
<script setup lang="ts">
import VaChart from '../va-charts/VaChart.vue';
import { computed } from 'vue'

const emits = defineEmits(['onDelete'])
type ChartTypes = "line" | "bar" | "bubble" | "doughnut" | "pie" | "horizontal-bar"

const props = defineProps<{
    chart: {
        type: ChartTypes
        data: Record<string, number>
    }
    index: number,
    label: string
    chartId: string
}>()

const colors = ['#2c82e0', '#ef476f', '#ffd166', '#06d6a0', '#8338ec', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#c9cbcf', '#e74c3c', '#3498db', '#2ecc71', '#f1c40f',
    '#e67e22', '#1abc9c', '#9b59b6', '#34495e', '#95a5a6', '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#f39c12',
    '#d35400', '#2c3e50', '#bdc3c7', '#7f8c8d', '#e74c3c', '#2980b9', '#f1c40f', '#2ecc71', '#9b59b6'
]


const chartOptions = computed(() => {
    const displayLegend = props.chart.type === 'doughnut' || props.chart.type === 'pie'
    const opts = {
        plugins: {
            title: {
                text: props.label,
                display: true,
                align: 'center'
            },
            datalabels: {
                color: '#ffffff',
                font: {
                    size: '18'
                }
            }, legend: { position: 'bottom', align: 'center', display: displayLegend }
        },

    }
    return opts
})
function createChartData(data: Record<string, number>) {
    const entries = Object.entries(data)

    const labels = entries.map(([k, v]) => k)

    return {
        labels: labels,
        datasets: [
            {
                backgroundColor: colors,
                data: Object.values(data),
                label: ''
            },
        ],
    }
}

function downloadCanvasAsPNG(canvasId: string, filename: string) {
    // Get the canvas element
    const canvas = document.getElementById(canvasId) as HTMLCanvasElement;

    // Ensure the canvas exists
    if (!canvas) {
        console.error('Canvas element not found!');
        return;
    }

    // Convert canvas to data URL
    const dataURL = canvas.toDataURL('image/png');

    // Create a download link
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = filename;

    // Trigger the download by simulating a click
    link.click();
}

</script>