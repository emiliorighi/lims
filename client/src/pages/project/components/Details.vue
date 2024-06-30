<template>
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardTitle class="va-text-secondary mb-0">Project details</VaCardTitle>
                <VaCardContent>
                    <MetadataTree :metadata="parsedDetails" />
                </VaCardContent>
            </VaCard>
        </div>
        <div class="flex lg6 md6 sm12 xs12">
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
        </div>
        <div v-if="experiment.id_format.length" class="flex lg6 md6 sm12 xs12">
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
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import MetadataTree from '../../../components/data/MetadataTree.vue';
import { useSchemaStore } from '../../../stores/schemas-store';


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

</script>