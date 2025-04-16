<template>
    <div class="row row-equal">
        <div class="flex lg6 md6 sm12 xs12">
            <VaCard>
                <VaCardActions>
                    <h2 class="va-h6">Model Fields</h2>
                </VaCardActions>
                <VaCardContent>
                    <FieldsAccordion :fields="fields" :id-format="idFormat" />
                </VaCardContent>
            </VaCard>
        </div>
        <div v-if="stats.length" class="flex lg6 md6 sm12 xs12">
            <ChartCard :chart="chart" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, watch } from 'vue';
import { useModelStore } from '../stores/model-store';
import FieldsAccordion from '../components/accordions/FieldsAccordion.vue';
import { useRecordStore } from '../stores/record-store';
import { useDateChart } from '../composables/chartConfigs';
import { useColors } from 'vuestic-ui/web-components';
import ChartCard from '../components/cards/ChartCard.vue';
import { ChartTypes } from '../data/types';

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

const colors = useColors()
const modelStore = useModelStore()
const recordStore = useRecordStore()
const fields = computed(() => modelStore.filters)
const idFormat = computed(() => modelStore.idFormat)
const stats = computed(() => recordStore.recordStats)
const query = computed(() => ({ project_id: props.projectId, model_name: props.modelName }))
const label = 'Records creation trend'
const chart = computed(() => {
    const freqs = Object.fromEntries(stats.value)

    const { labels, datasets, options } = useDateChart(freqs, label, colors.getColor('primary'))
    return {
        chartId: 'records_created',
        label,
        type: 'line' as ChartTypes,
        data: { datasets, labels },
        chartOptions: options
    }
})

watch(() => props.modelName, async () => {
    await recordStore.getRecordStats('created', query.value)
}, { immediate: true })


</script>