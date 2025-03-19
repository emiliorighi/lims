<template>
    <Header :title="title" />
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex">
                            <h5 class="va-h5">{{ schemaStore.schema.project_id }}</h5>
                        </div>
                        <div class="flex">
                            <div class="row">
                                <div class="flex">
                                    <VaButton preset="primary"
                                        @click="schemaStore.showSchema = !schemaStore.showSchema">
                                        View
                                    </VaButton>
                                </div>
                                <div class="flex">
                                    <DownloadYAMLProject :project="schemaStore.schema" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <VaAccordion v-model="accordion" class="max-w-sm">
                        <VaCollapse header="Project Details" icon="folder">
                            <div v-for="[k, v] in parsedDetails">
                                <div class="row">
                                    <div class="flex">
                                        <b> {{ k }} </b>
                                    </div>
                                    <div class="flex">
                                        <p>{{ v }}</p>
                                    </div>
                                </div>
                                <VaDivider />
                            </div>
                        </VaCollapse>
                        <VaCollapse v-for="opt in opts" :header="opt.label" :icon="opt.icon">
                            <VaDataTable :items="schemaStore.schema[opt.value].fields" :columns="columns">
                                <template #cell(type)="{ rowData }">
                                    {{ getFieldType(rowData) }}
                                </template>
                                <template #cell(actions)="{ rowData }">
                                    <VaChip @click="showFilterDetails(rowData)">View
                                    </VaChip>
                                </template>
                            </VaDataTable>
                        </VaCollapse>
                    </VaAccordion>
                </VaCardContent>
            </VaCard>
        </div>
        <div v-for="(card, index) in Object.values(cardsToShow)" :key="index"
            class="flex lg4 md4 sm12 xs12 cards-column">
            <ModelCountCard :card="card" />
        </div>
        <!-- <div v-if="samplesCreatedStats" class="flex lg4 md4 sm12 xs12">
            <DateChartCard title="Samples" :chart-data="createChartData(samplesCreatedStats, 'Samples created')" color="success" :count="cardsToShow.samples.count"
                icon="fa-vial" />
        </div> -->
    </div>
    <!-- 
   Create date line chart with samples and experiments
        
        -->
    <!-- <div class="flex lg8 md8 sm12 xs12">
            <VaCard v-if="expData && sampleData">

                <VaCardContent style="height: 400px;">
                    <VaChart :options="chartOptions" type="horizontal-bar"
                        :data="createChartData(sampleData, expData)" />
                </VaCardContent>
            </VaCard>
            <VaSkeleton v-else height="400px" />
        </div> -->
    <!-- <div class="flex lg4 md4 sm12 xs12 cards-column">
            <div v-for="(card, index) in Object.values(cardsToShow)" :key="index" class="row row-equal card-wrapper">
                <div class="flex lg12 md12 sm12 xs12">
                    <ModelCountCard :card="card" />
                </div>
            </div>
        </div> -->



    <VaModal v-if="selectedFilter" max-height="500px" fixed-layout v-model="showDetails">

        <template #header>
            <div class="row align-center justify-space-between">
                <h3 class=" flex va-h3">
                    {{ selectedFilter.key }}
                </h3>
            </div>
        </template>
        <VaDivider />
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <MetadataTree :metadata="Object.entries(selectedFilter)" />
            </div>
        </div>

    </VaModal>
    <ProjectDetailsModal />

</template>
<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useSchemaStore } from '../../../stores/schema-store';
import DownloadYAMLProject from '../../../components/buttons/DownloadYAMLProject.vue'
import Header from '../../../components/ui/Header.vue'
import { Filter, ModelType } from '../../../data/types'
import ModelCountCard from '../../../components/cards/ModelCountCard.vue'
import MetadataTree from '../../../components/ui/MetadataTree.vue';
import ProjectService from '../../../services/clients/ProjectService'
import ProjectDetailsModal from '../../../components/modals/ProjectDetailsModal.vue'
import DateChartCard from '../../../components/cards/DateChartCard.vue'

const props = defineProps<{
    title: string
}>()


const columns = [
    { key: "key", sortable: true },
    { key: "label", sortable: true },
    { key: "required" },
    { key: "type" },
    { key: "actions" }
]
const collapseOptions = [
    { label: 'Sample Definitions', value: 'sample' as ModelType, icon: 'fa-vial' },
    { label: 'Experiment Definitions', value: 'experiment' as ModelType, icon: 'fa-dna' }
]


const selectedFilter = ref<Filter | undefined>()
const schemaStore = useSchemaStore()
const { sample, experiment, ...details } = schemaStore.schema
// const samplesCreatedStats = ref<Record<string, any> | undefined>()
// const expCreatedStats = ref<Record<string, any> | undefined>()

const accordion = ref([false, false, false])
const showDetails = ref(false)
const cards = reactive({
    samples: { icon: 'fa-vial', text: 'Samples', color: 'success', count: 0 },
    experiments: { icon: 'fa-dna', text: 'Experiments', color: 'primary', count: 0 },
    users: { icon: 'group', text: 'Users', color: 'secondary', count: 0 }
});

const hasExperiments = computed(() => {
    return experiment.fields.length > 0
})

const cardsToShow = computed(() => {
    const { samples, experiments, users } = cards
    if (hasExperiments.value) return { samples, experiments, users }
    return { samples, users }
})

const opts = computed(() => {
    if (hasExperiments.value) return collapseOptions
    return collapseOptions.filter(f => f.value !== 'experiment')
})

const parsedDetails = computed(() => {
    const dets = Object.entries(details).filter(([k, v]) => k !== 'created')
    if (details.created && details.created.$date) {
        const parsedTime = parseTimestamp(details.created.$date)
        dets.push(['created', parsedTime])
    }
    return dets
})

onMounted(async () => {
    await lookupProjectData(details.project_id)
    // const samplesResp = await ProjectService.getProjectStats(details.project_id, 'samples', 'created')
    // samplesCreatedStats.value = { "2024-10-12":10, "2023-10-12":10,  ...samplesResp.data, }
    // const expResp = await ProjectService.getProjectStats(details.project_id, 'experiments', 'created')
    // expCreatedStats.value = { ...expResp.data }
})




function getFieldType(item: Filter): 'input' | 'select' | 'range' {
    const filterKeys = Object.keys(item.filter)
    if (filterKeys.includes('input_type')) return 'input'
    if (filterKeys.includes('choices')) return 'select'
    return 'range'
}

async function lookupProjectData(id: string) {
    try {
        const { data } = await ProjectService.lookupProject(id)
        const { samples, experiments, users } = data
        cards.samples.count = samples
        cards.experiments.count = experiments
        cards.users.count = users
    } catch (e) {
        console.error(e)
    }
}

// function getModelStats(model: ModelType, field: string) {
//     try {
//         const { data } = await ProjectService.getProjectStats(details.project_id, model, field)

//     } catch (err) {
//         console.log(err)
//     }
// }

function showFilterDetails(rowData: Filter) {
    selectedFilter.value = { ...rowData }
    showDetails.value = !showDetails.value
}

function parseTimestamp(timestamp: number): string {
    // Create a Date object from the timestamp
    const date = new Date(timestamp);

    // Extract date components
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    // Format the date as "YYYY-MM-DD HH:MM:SS"
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function createChartData(data: Record<string, number>, label: string) {


    return {
        labels: Object.keys(data),
        datasets: [
            {
                backgroundColor: 'rgba(75,192,192,0.4)',
                label: label,
                data: Object.values(data),
            },
        ]
    }
}

</script>

<style scoped>
.cards-column {
    display: flex;
    flex-direction: column;
}

.card-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
}
</style>