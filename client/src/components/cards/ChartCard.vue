<template>
    <VaCard>
        <VaCardActions align="between">
            
            <h2 class="va-h6">{{ chart.label }}</h2>
            <VaButton size="small" color="textPrimary" preset="primary"
                @click="downloadCanvasAsPNG(chart.chartId, `${chart.chartId}.png`)">Download</VaButton>
        </VaCardActions>
        <VaCardContent style="height: 400px;">
            <component :is="chartComponent" ref="chart" class="va-chart" :chart-id="chart.chartId"
                :chart-options="chart.chartOptions" :chart-data="chart.data" />
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { chartTypesMap } from '../../composables/chartConfigs';
import { computed } from 'vue'
import { ChartItem } from '../../data/types';

const emits = defineEmits(['onDelete'])

const props = defineProps<{
    chart: ChartItem
}>()

const chartComponent = computed(() => chartTypesMap[props.chart.type])

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