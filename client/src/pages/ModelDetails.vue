<template>
    <div class="row">
        <div class="flex lg3 md4 sm12 xs12">
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AttributesCard />
                </div>
            </div>
            <div v-if="refModel" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard>
                        <VaCardContent>
                            <div class="row">
                                <div class="flex">
                                    <h2 class="va-h4">Reference Model</h2>
                                    <p class="va-text-secondary">
                                        The model referenced by {{ modelName }}
                                    </p>
                                </div>
                            </div>
                        </VaCardContent>
                        <VaCardContent>
                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaButton :to="{ name: 'details', params: { projectId, modelName: refModel.name } }"
                                        color="backgroundElement" icon-right="fa-arrow-up-right-from-square" block>{{
                                            refModel.name }}</VaButton>
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>
            <div v-if="relatedModels && relatedModels.length" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard>
                        <VaCardContent>
                            <div class="row">
                                <div class="flex">
                                    <h2 class="va-h4">Related Models</h2>
                                    <p class="va-text-secondary">
                                        The models that reference {{ modelName }}
                                    </p>
                                </div>
                            </div>
                        </VaCardContent>
                        <VaCardContent>
                            <div class="row">
                                <div v-for="m in relatedModels" class="flex lg12 md12 sm12 xs12">
                                    <VaButton :to="{ name: 'details', params: { projectId, modelName: m.name } }"
                                        color="backgroundElement" icon-right="fa-arrow-up-right-from-square" block>{{
                                            m.name }}</VaButton>
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>
        </div>
        <div v-if="stats.length" class="flex lg9 md8 sm12 xs12">
            <ChartCard :chart="chart" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useRecordStore } from '../stores/record-store';
import { useDateChart } from '../composables/chartConfigs';
import { useColors } from 'vuestic-ui/web-components';
import ChartCard from '../components/cards/ChartCard.vue';
import { ChartTypes } from '../data/types';
import AttributesCard from '../components/cards/AttributesCard.vue';
import { useProjectStore } from '../stores/project-store';
import { useModelStore } from '../stores/model-store';

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

const colors = useColors()
const recordStore = useRecordStore()
const projectStore = useProjectStore()
const modelStore = useModelStore()
const models = computed(() => projectStore.schema?.models)
const relatedModels = computed(() => models.value?.filter(({ reference_model }) => reference_model === props.modelName))
const refModel = computed(() => modelStore.refModel)
const stats = computed(() => recordStore.recordStats)
const query = computed(() => ({ project_id: props.projectId, model_name: props.modelName }))
const label = 'Records by creation date'

const chart = computed(() => {
    const freqs = Object.fromEntries(stats.value)

    const { labels, datasets, options } = useDateChart(freqs, label, colors.getColor('primary'))
    return {
        chartId: 'records_created',
        label,
        type: 'line' as ChartTypes,
        data: { datasets, labels },
        chartOptions: options,
        description: 'Trend of records by creation date '
    }
})

onMounted(async () => {
    //get related models
    //get models that references this model
})

watch(() => props.modelName, async () => {
    await recordStore.getRecordStats('created', query.value)
}, { immediate: true })


</script>