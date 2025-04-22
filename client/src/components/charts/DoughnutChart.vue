<template>
  <Doughnut :chart-id="chartId" :chart-options="chartOptions" :chart-data="props.chartData" />
</template>

<script setup lang="ts">
  import { Doughnut } from 'vue-chartjs'
  import type { TChartOptions } from 'vue-chartjs/dist/types'
  import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'
  import { TDoughnutChartData } from '../../data/types'
  import ChartDataLabels from 'chartjs-plugin-datalabels';

  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale,ChartDataLabels)

  const props = defineProps<{
    chartData: TDoughnutChartData
    chartOptions?: TChartOptions<'doughnut'>
    chartId?: string

  }>()
</script>
