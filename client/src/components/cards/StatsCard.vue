<template>
    <VaCard color="backgroundElement">
        <VaCardActions align="end">
            <VaButton preset="primary" @click="downloadCanvasAsPNG(chartId, `${chartId}.png`)">Download</VaButton>
        </VaCardActions>
        <VaCardContent style="height: 400px;">
            <component :is="chartComponent" ref="chart" class="va-chart" :chart-id="chartId"
            :chart-options="chartOptions" :chart-data="data" />
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { chartTypesMap } from '../../composables/chartConfigs';
import { computed } from 'vue'

const emits = defineEmits(['onDelete'])
type ChartTypes = "line" | "bar" | "bubble" | "doughnut" | "pie" | "horizontal-bar"

const props = defineProps<{
    type:ChartTypes
    data:any
    label: string
    chartId: string
    chartOptions:any
}>()

const chartComponent = computed(() => chartTypesMap[props.type])

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