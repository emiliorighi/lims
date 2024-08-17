<template>
    <Header :title="title" />
    <div class="row row-equal">
      <div class="flex lg8 md8 sm12 xs12">
        <VaCard v-if="chartData">
          <VaCardContent style="height: 400px;">
            <VaChart :options="chartOptions" type="horizontal-bar" :data="chartData" />
          </VaCardContent>
        </VaCard>
        <VaSkeleton v-else height="400px" />
      </div>
      <div class="flex lg4 md4 sm12 xs12 cards-column">
        <div v-for="(card, index) in Object.values(cards)" :key="index" class="card-wrapper">
          <ModelCountCard :card="card" />
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted, ref, computed } from 'vue';
  import StatsService from '../../services/clients/StatsService';
  import VaChart from '../../components/va-charts/VaChart.vue';
  import ModelCountCard from '../../components/cards/ModelCountCard.vue';
  import Header from '../../components/ui/Header.vue';
  
  const props = defineProps<{ title: string }>();
  
  const expData = ref<Record<string, number> | null>(null);
  const sampleData = ref<Record<string, number> | null>(null);
  const cards = ref({
    samples: { icon: 'fa-vial', text: 'Samples', color: 'success', count: 0 },
    experiments: { icon: 'fa-dna', text: 'Experiments', color: 'primary', count: 0 },
    projects: { icon: 'folder', text: 'Projects', color: 'secondary', count: 0 }
  });
  
  const chartOptions = {
    plugins: {
      title: {
        text: 'Number of Samples and Experiments by Project',
        display: true,
        align: 'start'
      },
      datalabels: {
        color: '#ffffff',
        font: { size: 18 }
      },
      legend: { position: 'bottom', align: 'center' }
    }
  };
  
  const chartData = computed(() => {
    if (!sampleData.value || !expData.value) return null;
    return createChartData(sampleData.value, expData.value);
  });
  
  onMounted(async () => {
    try {
      const [samplesStats, experimentsStats, counts] = await Promise.all([
        getStats('samples'),
        getStats('experiments'),
        lookupData()
      ]);
  
      sampleData.value = samplesStats;
      expData.value = experimentsStats;
  
      cards.value.samples.count = counts.samples;
      cards.value.experiments.count = counts.experiments;
      cards.value.projects.count = counts.projects;
    } catch (err) {
      console.error('Error loading data:', err);
    }
  });
  
  async function lookupData() {
    try {
      const { data } = await StatsService.lookupData();
      return data;
    } catch (error) {
      console.error('Error fetching lookup data:', error);
      return { samples: 0, experiments: 0, projects: 0 };
    }
  }
  
  async function getStats(model: 'samples' | 'experiments') {
    try {
      const { data } = await StatsService.getStats(model, 'project');
      return data;
    } catch (err) {
      console.error(`Error fetching ${model} stats:`, err);
      return {};
    }
  }
  
  function createChartData(sampleData: Record<string, number>, experimentData: Record<string, number>) {
    const uniqueLabels = Array.from(new Set([...Object.keys(sampleData), ...Object.keys(experimentData)]));
  
    const datasets = [
      {
        backgroundColor: '#2c82e0',
        label: 'Samples',
        data: uniqueLabels.map(label => sampleData[label] || 0)
      },
      {
        backgroundColor: '#ef476f',
        label: 'Experiments',
        data: uniqueLabels.map(label => experimentData[label] || 0)
      }
    ];
  
    return { labels: uniqueLabels, datasets };
  }
  </script>
  
  <style scoped>
  .cards-column {
    display: flex;
    flex-direction: column;
  }
  
  .card-wrapper {
    margin-bottom: 1rem; /* Adjusts space between cards */
  }
  </style>
  