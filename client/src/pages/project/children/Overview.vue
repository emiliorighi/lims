<template>
    <Header :title="title" />
    <div class="row">
        <div class="flex">
            <VaCard>
                <VaCardTitle class="va-text-secondary">
                    Project details
                </VaCardTitle>
                <VaCardContent>
                    <ul>
                        <li v-for="[k, v] in parsedDetails.filter(([k, v]) => v)">
                            <h4 class="va-h4">{{ v }}</h4>
                            <p class="va-text-secondary"> {{ k }} </p>
                        </li>
                    </ul>
                    <h3></h3>
                    <!-- <MetadataTree :metadata="Object.entries(parsedDetails)" /> -->
                </VaCardContent>
            </VaCard>
        </div>
        <!-- <div class="flex lg8 md8 sm12 xs12">
            <VaCard v-if="expData && sampleData">

                <VaCardContent style="height: 400px;">
                    <VaChart :options="chartOptions" type="horizontal-bar"
                        :data="createChartData(sampleData, expData)" />
                </VaCardContent>
            </VaCard>
            <VaSkeleton v-else height="400px" />
        </div> -->
        <div class="flex lg4 md6 sm12 xs12">
            <VaCard>
                <VaCardTitle class="va-text-secondary">
                    Metadata Definitions
                </VaCardTitle>
                <VaCardContent>
                    <div class="row justify-space-between align-center">
                        <div class="flex">
                            <VaSwitch :disabled="switchDisabled" v-model="switchValue" color="success"
                                off-color="primary" true-value="sample" false-value="experiment"
                                style="--va-switch-checker-background-color: #252723;">
                                <template #innerLabel>
                                    <div class="va-text-center">
                                        <VaIcon :name="switchValue === 'sample' ? 'fa-vial' : 'fa-dna'" />
                                    </div>
                                </template>
                            </VaSwitch>
                        </div>
                        <div class="flex">
                            <div class="row">
                                <div class="flex">
                                    <VaButton preset="primary"
                                        @click="schemaStore.showSchema = !schemaStore.showSchema">
                                        View Schema
                                    </VaButton>
                                </div>
                                <div class="flex">
                                    <DownloadYAMLProject :project="schemaStore.schema" />
                                </div>
                            </div>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <VaDataTable sticky-header height="300px" :items="attributes" :columns="columns">
                        <template #cell(type)="{ rowData }">
                            <VaChip @click="showFilterDetails(rowData)">{{
        getFieldType(rowData)
    }}</VaChip>
                        </template>
                    </VaDataTable>
                </VaCardContent>
            </VaCard>
        </div>
        <!-- <div class="flex lg4 md4 sm12 xs12 cards-column">
            <div v-for="(card, index) in Object.values(cardsToShow)" :key="index" class="row row-equal card-wrapper">
                <div class="flex lg12 md12 sm12 xs12">
                    <ModelCountCard :card="card" />
                </div>
            </div>
        </div> -->
    </div>
    <VaCard>
        <VaCardContent>
            <div class="row justify-space-between align-center">
                <div class="flex">
                    <VaSwitch :disabled="switchDisabled" v-model="switchValue" color="success" off-color="primary"
                        true-value="sample" false-value="experiment"
                        style="--va-switch-checker-background-color: #252723;">
                        <template #innerLabel>
                            <div class="va-text-center">
                                <VaIcon :name="switchValue === 'sample' ? 'fa-vial' : 'fa-dna'" />
                            </div>
                        </template>
                    </VaSwitch>
                </div>
                <div class="flex">
                    <div class="row">
                        <div class="flex">
                            <VaButton preset="primary" @click="schemaStore.showSchema = !schemaStore.showSchema">
                                View Schema
                            </VaButton>
                        </div>
                        <div class="flex">
                            <DownloadYAMLProject :project="schemaStore.schema" />
                        </div>
                    </div>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <VaDataTable sticky-header height="300px" :items="attributes" :columns="columns">
                <!-- <template #header(model)>
                    <VaCardActions class="p-0" align="center">
                        <VaButton :color="sampleCount > 0 ? 'success' : 'danger'" icon="fa-vial">Sample {{ sampleCount
                            }}
                        </VaButton>
                        <VaButton :color="experimentCount > 0 ? 'info' : 'warning'" icon="fa-dna">Experiment {{
        experimentCount
    }}
                        </VaButton>
                    </VaCardActions>
                </template> -->
                <template #cell(type)="{ rowData }">
                    <VaChip @click="showFilterDetails(rowData)">{{
        getFieldType(rowData)
    }}</VaChip>
                </template>
            </VaDataTable>
        </VaCardContent>
        <!-- 
            number of sample and experiments cards
            project info 
            charts?
            sample fields
            experiment fields
        
        -->
    </VaCard>


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
    <!-- 
    bar chart with samples and experiments
    
    
    -->
    <div class="row">
        <!-- <div class="flex lg6 md6 sm12 xs12">
            <VaCardContent style="height: 400px;">
                <VaChart type="horizontal-bar" :data="chartData" />
            </VaCardContent>
            <VaCard>
                <VaCardTitle class="va-text-secondary mb-0">Project details</VaCardTitle>
                <VaCardContent>
                    <MetadataTree :metadata="parsedDetails" />
                </VaCardContent>
            </VaCard>
        </div> -->
        <!-- <div class="flex lg6 md6 sm12 xs12">
            <VaCard>
                <VaCardTitle class="va-text-secondary mb-0">
                    <div class="row justify-space-between">
                        <div class="flex p-0"> Sample Definitions</div>
                        <div class="flex p-0">
                            <VaIcon name="fa-vial" style="margin-left: 3px;" />
                        </div>
                    </div>
                </VaCardTitle>
                <VaCardContent>
                    <MetadataTree :metadata="Object.entries(sample)" />
                </VaCardContent>
            </VaCard>
        </div> -->
        <!-- <div v-if="experiment.id_format.length" class="flex lg6 md6 sm12 xs12">
            <VaCard>
                <VaCardTitle class="va-text-secondary mb-0">
                    <div class="row justify-space-between">
                        <div class="flex p-0"> Experiment Definitions</div>
                        <div class="flex p-0">
                            <VaIcon name="fa-dna" style="margin-left: 3px;" />
                        </div>
                    </div>
                </VaCardTitle>
                <VaCardContent>
                    <MetadataTree :metadata="Object.entries(experiment)" />
                </VaCardContent>
            </VaCard>
        </div> -->
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useSchemaStore } from '../../../stores/schemas-store';
import DownloadYAMLProject from '../../../components/buttons/DownloadYAMLProject.vue'
import Header from '../../../components/ui/Header.vue'
import { Filter, ModelType } from '../../../data/types'
import ModelCountCard from '../../../components/cards/ModelCountCard.vue'
import MetadataTree from '../../../components/ui/MetadataTree.vue';
import ProjectService from '../../../services/clients/ProjectService'

const props = defineProps<{
    title: string
}>()

const switchValue = ref<ModelType>('sample')
const showDetails = ref(false)
const lookupData = ref<LookupResponse>({ samples: 0, experiments: 0 })
const chartOptions = {
    plugins: {
        title: {
            text: 'Number of Samples and Experiments',
            display: true,
            align: 'start'
        },
        datalabels: {
            color: '#ffffff',
            font: {
                size: '18'
            }
        },
        legend: { position: 'bottom', align: 'center' }
    },

}
type LookupResponse = {
    samples: number
    experiments: number
}

const selectedFilter = ref<Filter | undefined>()
const schemaStore = useSchemaStore()

const { sample, experiment, ...details } = schemaStore.schema

onMounted(async () => {
    await lookupProjectData(details.project_id)
})
const switchDisabled = computed(() => {
    return experiment.id_format.length === 0
})

const attributes = computed(() => {
    return switchValue.value === 'sample' ? sample.fields : experiment.fields
})

// const dataToShow = computed(() => {
//     const { samples, experiments } = cards.value
//     if (switchDisabled.value) return { samples }
//     return { samples, experiments }
// })


const parsedDetails = computed(() => {
    const dets = Object.entries(details).filter(([k, v]) => k !== 'created')
    if (details.created && details.created.$date) {
        const parsedTime = parseTimestamp(details.created.$date)
        dets.push(['created', parsedTime])
    }
    return dets
})
const columns = [
    { key: "key", sortable: true },
    { key: "required", sortable: true },
    { key: "type", width: 120 },
]

function getFieldType(item: Filter): 'input' | 'select' | 'range' {
    const filterKeys = Object.keys(item.filter)
    if (filterKeys.includes('input_type')) return 'input'
    if (filterKeys.includes('choices')) return 'select'
    return 'range'
}
async function lookupProjectData(id: string) {
    try {
        const { data } = await ProjectService.lookupProject(id)
        const { samples, experiments } = data
        lookupData.value = { samples, experiments }
    } catch (e) {

    }

}

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

function createChartData(lookupData: LookupResponse) {


    return {
        labels: ['Samples', 'Experiments'],
        datasets: [
            {
                backgroundColor: '#2c82e0',
                label: '',
                data: [lookupData.samples, lookupData.experiments],
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