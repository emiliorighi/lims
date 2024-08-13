<template>
    <VaModal max-height="500px" fixed-layout v-model="schemaStore.showDetails">
        <template #header>
            <div class="row align-center justify-space-between">
                <h3 class=" flex va-h3">
                    {{ 'experiment_id' in item ? item.experiment_id : item.sample_id }}
                </h3>
                <VaIcon color="primary" size="large" class="flex" :name="icon" />

            </div>
        </template>
        <VaDivider/>
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <MetadataTree :metadata="Object.entries(item.metadata)" />
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { ExperimentModel, SampleModel } from '../../data/types';
import MetadataTree from '../ui/MetadataTree.vue';
import { computed } from 'vue'

const props = defineProps<{
    item: SampleModel | ExperimentModel,
}>()

const schemaStore = useSchemaStore()

const icon = computed(() => {
    return 'experiment_id' in props.item ? 'fa-dna' : 'fa-vial'
})
</script>