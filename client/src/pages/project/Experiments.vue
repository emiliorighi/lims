<template>
    <DataManagement v-if="schemaStore.model === 'experiment'" :title="title"
        :itemStore="useExperimentStore" :description="description" :addButtonLabel="buttonLabel" />
</template>

<script setup lang="ts">
import { useExperimentStore } from '../../stores/experiment-store'
import { useSchemaStore } from '../../stores/schemas-store'

import DataManagement from './components/DataManagement.vue'
import { computed, onMounted } from 'vue'

const title = 'Experiments'
const buttonLabel = 'Add Experiment'
const schemaStore = useSchemaStore()
const description = computed(() => {
    return `List of experiments related to project ${schemaStore.schema.project_id}`
})
onMounted(() => {
    schemaStore.model = 'experiment'
})

</script>
