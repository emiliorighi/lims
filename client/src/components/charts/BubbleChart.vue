<template>
  <Bubble :chart-id="chartId" :chart-options="chartOptions" :chart-data="props.chartData" />
</template>

<script setup lang="ts">
  import { Bubble } from 'vue-chartjs'
  import type { TChartOptions } from 'vue-chartjs/dist/types'
  import { Chart as ChartJS, Title, Tooltip, Legend, PointElement, LinearScale } from 'chart.js'
  import { TBubbleChartData } from '../../../data/types'
  import ChartDataLabels from 'chartjs-plugin-datalabels';

  ChartJS.register(Title, Tooltip, Legend, PointElement, LinearScale,ChartDataLabels)

  const props = defineProps<{
    chartData: TBubbleChartData
    chartOptions?: TChartOptions<'bubble'>
    chartId?: string

  }>()
</script>
