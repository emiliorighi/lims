<template>
  <Bar :chart-id="chartId" :chart-options="chartOptions" :chart-data="props.chartData" />
</template>

<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import type { TChartOptions } from 'vue-chartjs/dist/types'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, LinearScale, CategoryScale } from 'chart.js'
import { TBarChartData } from '../../data/types'
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, Tooltip, Legend, BarElement, LinearScale, CategoryScale, ChartDataLabels)

const props = defineProps<{
  chartData: TBarChartData
  chartOptions?: TChartOptions<'bar'>
  chartId?: string
}>()
</script>
