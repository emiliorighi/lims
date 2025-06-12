<template>
    <div>
        <ModelForm v-if="showModelForm" from-project mode="create" :existing-models="projectStore.models" @submit="handleNewModel" @close="handleClose" />
        <div v-else>
            <div class="row justify-space-between align-center mb-4">
                <div class="flex">
                    <h1 class="va-h1">Project Dashboard</h1>
                    <p class="va-text-secondary">
                        Details and stats of {{ projectId }}
                    </p>
                </div>
                <div v-if="role === 'admin' || role === 'project_manager'" class="flex">
                    <div class="row align-center">
                        <div class="flex mr-2">
                            <VaButton :disabled="projectStore.isLoading" @click="projectStore.showArchiveModal = true"
                                :color="isArchived ? 'success' : 'warning'"
                                :icon="isArchived ? 'fa-unlock' : 'fa-lock'">
                                {{ isArchived ? 'Reactivate' : 'Archive' }} Project
                            </VaButton>
                        </div>
                        <div class="flex">
                            <VaButton :disabled="isArchived || projectStore.isLoading"
                                @click="showModelForm = true" color="primary" icon="fa-plus">
                                New Model
                            </VaButton>
                        </div>
                    </div>
                </div>
            </div>
            <VaInnerLoading :loading="projectStore.isLoading">
                <div class="row">
                    <div v-for="model in mappedModels" class="flex lg4 md6 sm12 xs12">
                        <VaSkeleton v-if="modelStats[model.name]?.isLoading" class="mb-4" variant="squared" />
                        <VaCard v-else class="mb-4">
                            <VaCardContent>
                                <div class="row align-center">
                                    <div class="flex">
                                        <div class="row align-center">
                                            <div class="flex">
                                                <VaIcon color="neutral" name="fa-cube" />
                                            </div>
                                            <div class="flex">
                                                <VaButton
                                                    :to="{ name: 'details', params: { modelName: model.name, projectId: projectId } }"
                                                    class="pa-0" color="textPrimary" preset="plain">
                                                    <h2 class="va-h3">{{ model.name }}</h2>
                                                </VaButton>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex">
                                        <VaChip v-if="model.refModel" color="backgroundElement" size="small"
                                            icon="fa-link">
                                            {{ model.refModel }}
                                        </VaChip>
                                    </div>
                                </div>
                            </VaCardContent>
                            <VaCardContent>
                                <div class="row align-center">
                                    <ModelStatItem label="Records" route-name="records" :model-name="model.name"
                                        :project-id="projectId" :value="model.counts" />
                                    <ModelStatItem label="Protocols" route-name="protocols" :model-name="model.name"
                                        :project-id="projectId" :value="modelStats[model.name]?.protocols" />
                                    <ModelStatItem label="Images" route-name="images" :model-name="model.name"
                                        :project-id="projectId" :value="modelStats[model.name]?.images" />
                                </div>
                            </VaCardContent>
                        </VaCard>
                    </div>
                </div>

                <div class="row row-equal">
                    <div v-for="chart in charts" class="flex lg4 md6 sm12 xs12">
                        <ChartCard :key="chart.chartId" :chart="chart" class="mb-4"></ChartCard>
                    </div>
                </div>
            </VaInnerLoading>

            <!-- Modals -->
            <ArchiveProjectModal :archive="!isArchived" :project-id="projectId" />
        </div>

    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useProjectStore } from '../stores/project-store';
import { useGlobalStore } from '../stores/global-store';
import { useModelStore } from '../stores/model-store';
import { getChartOptions, processChartData } from '../composables/chartConfigs';
import { ChartTypes, ResearchModel } from '../data/types';
import ChartCard from '../components/cards/ChartCard.vue';
import ArchiveProjectModal from '../components/modals/ArchiveProjectModal.vue';
import { useToast } from 'vuestic-ui';
import AuthService from '../services/clients/AuthService';
import { catchError } from '../composables/toastMessages';
import StatsService from '../services/clients/StatsService';
import ModelStatItem from '../components/ModelStatItem.vue';
import ModelForm from '../components/forms/ModelForm.vue';

const props = defineProps<{
    projectId: string
}>();

const { init } = useToast();
const queryField = 'model_name';
const showModelForm = ref(false)
const globalStore = useGlobalStore();
const projectStore = useProjectStore();
const modelStore = useModelStore();
const role = computed(() => globalStore.user.role)
const mappedModels = computed(() => projectStore.mappedModels);
const recordStats = computed(() => globalStore.recordStats);
const isArchived = computed(() => projectStore.isArchived);

const charts = computed(() => {
    const charts = [];
    if (recordStats.value.length) {
        charts.push(createChart(
            Object.fromEntries(recordStats.value),
            queryField,
            'Records by model',
            'doughnut',
            'Number of records across the models'
        ));
    }
    return charts;
});

const modelStats = ref<Record<string, { protocols: number, images: number, isLoading: boolean }>>({});

onMounted(async () => {
    await globalStore.lookupData();
    await projectStore.getProjectStats(props.projectId);
    await projectStore.getProjectStatus(props.projectId);
    await globalStore.getLinkStats(queryField, 'images', { project_id: props.projectId });
    await globalStore.getLinkStats(queryField, 'protocols', { project_id: props.projectId });
    await globalStore.getRecordStats(queryField, { project_id: props.projectId });

    // Fetch stats for each model
    for (const model of mappedModels.value) {
        modelStats.value[model.name] = { protocols: 0, images: 0, isLoading: true };
        try {
            const { data } = await StatsService.getModelStats(props.projectId, model.name);
            modelStats.value[model.name] = {
                protocols: data.protocols || 0,
                images: data.images || 0,
                isLoading: false
            };
        } catch (error) {
            catchError(error);
            modelStats.value[model.name].isLoading = false;
        }
    }
});

function handleClose() {
    showModelForm.value = false;
}

async function handleNewModel(model: ResearchModel) {
    try {
        await AuthService.createModel(props.projectId, model);
        init({ color: 'success', message: `Model ${model.name} created successfully` });
        await projectStore.getProjectSchema(props.projectId);
        await projectStore.getProjectStats(props.projectId);
        showModelForm.value = false;
    } catch (error) {
        catchError(error);
    }
}

function createChart(frequencies: Record<string, number>, fieldKey: string, label: string, type: ChartTypes, description?: string) {
    const data = processChartData(frequencies, fieldKey);
    const chartOptions = getChartOptions(type);
    return {
        chartId: label,
        chartOptions,
        type: type,
        data,
        label,
        description
    };
}
</script>

<style scoped>
.mb-4 {
    margin-bottom: 1rem;
}

.mr-2 {
    margin-right: 0.5rem;
}

.mr-4 {
    margin-right: 1rem;
}

.ml-1 {
    margin-left: 0.25rem;
}

.pa-0 {
    padding: 0 !important;
}
</style>