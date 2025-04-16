<template>
  <div>
    <div class="row align-end justify-space-between">
      <div class="flex">
        <h1 class="va-h1">Dashboard</h1>
      </div>
    </div>
    <div class="row row-equal">
      <div v-for="([k, v]) in counts" class="flex lg2 md3 sm6 xs6">
        <VaCard>
          <VaCardContent>
            <div class="row align-center">
              <div class="flex">
                <VaIcon color="secondary" size="2rem" :name="iconMap[k as ModelKeys]" />
              </div>
              <div class="flex">
                <h2 class="va-h4 va-text-capitalize">{{ k }}</h2>
              </div>
              <div class="flex lg12 md12 sm12 xs12">
                <Counter :duration="2000" :target-value="v" />
              </div>
            </div>
          </VaCardContent>
        </VaCard>
      </div>
    </div>
    <div v-if="charts.length" class="row">
      <div v-for="chart in charts" class="flex lg6 md6 sm12 xs12">
        <ChartCard :chart="chart"></ChartCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, } from 'vue';
import Counter from '../components/ui/Counter.vue';
import { useGlobalStore } from '../stores/global-store';
import { getChartOptions, processChartData } from '../composables/chartConfigs';
import ChartCard from '../components/cards/ChartCard.vue';
import { ChartTypes, ModelKeys } from '../data/types';

const queryField = 'project_id'

const globalStore = useGlobalStore()


const iconMap: Record<ModelKeys, string> = {
  projects: 'fa-diagram-project',
  models: 'fa-cube',
  protocols: 'fa-scroll',
  records: 'fa-file-lines',
  images: 'fa-image'
}

const counts = computed(() => Object.entries(globalStore.counts))
const recordStats = computed(() => globalStore.recordStats)
const protocolStats = computed(() => globalStore.protocolStats)
const imagesStats = computed(() => globalStore.imageStats)

const charts = computed(() => {
  const charts = []
  if (recordStats.value.length) charts.push(createChart(Object.fromEntries(recordStats.value), queryField, 'Records by project', 'horizontal-bar'))
  if (protocolStats.value.length) charts.push(createChart(Object.fromEntries(protocolStats.value), queryField, 'Protocols by project', 'doughnut'))
  if (imagesStats.value.length) charts.push(createChart(Object.fromEntries(imagesStats.value), queryField, 'Images by project', 'doughnut'))
  return charts
})

onMounted(async () => {
  await globalStore.lookupData()
  await globalStore.getProtocolStats(queryField, {})
  await globalStore.getRecordStats(queryField, {})
  await globalStore.getImagesStats(queryField, {})
});


function createChart(frequencies: Record<string, number>, fieldKey: string, label: string, type: ChartTypes) {

  const data = processChartData(frequencies, fieldKey);
  const chartOptions = getChartOptions(type);
  return {
    chartId: label,
    chartOptions,
    type: type,
    data,
    label
  }
}



</script>
