<template>
    <Header :title="title" />
    <div class="row justify-space-between align-center">
        <div class="flex p-0">
            <h4 class="va-h4">Overview</h4>
            <p class="va-text-secondary mb-4">Project Overview</p>
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
    <div class="row justify-space-between row-equal">
        <div class="flex">

        </div>
    </div>

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
import { computed } from 'vue';
import MetadataTree from '../../../components/ui/MetadataTree.vue';
import { useSchemaStore } from '../../../stores/schemas-store';
import ProjectService from '../../../services/clients/ProjectService'
import VaChart from '../../../components/va-charts/VaChart.vue'
import DownloadYAMLProject from '../../../components/buttons/DownloadYAMLProject.vue'
import Header from '../../../components/ui/Header.vue'

const props = defineProps<{
    title: string
}>()

type LookupResponse = {
    samples: number
    experiments: number
}

const schemaStore = useSchemaStore()

const { sample, experiment, ...details } = schemaStore.schema


const parsedDetails = computed(() => {
    const dets = Object.entries(details).filter(([k, v]) => k !== 'created')
    if (details.created && details.created.$date) {
        const parsedTime = parseTimestamp(details.created.$date)
        dets.push(['created', parsedTime])
    }
    return dets
})

// async function lookupProjectData(id: string) {
//     try {
//         const { data } = await ProjectService.lookupProject(id)
//     }

// }
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
                label: 'Samples',
                data: [lookupData.samples, lookupData.experiments],
            },
            // {
            //     backgroundColor: '#ef476f',
            //     label: 'Experiments',
            //     data: orderedExperimentEntries.map(([k, v]) => v),
            // }
        ]
    }
}

</script>