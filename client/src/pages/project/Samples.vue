<template>
    <DataManagement v-if="schemaStore.model === 'sample'" :title="title" :itemStore="useSampleStore"
        :description="description" :addButtonLabel="buttonLabel" />
</template>

<script setup lang="ts">
import { useSampleStore } from '../../stores/sample-store'
import { useSchemaStore } from '../../stores/schemas-store'

import DataManagement from './components/DataManagement.vue'
import { computed, onMounted } from 'vue'

const title = 'Samples'
const buttonLabel = 'Add Sample'
const schemaStore = useSchemaStore()
const description = computed(() => {
    return `List of samples related to project ${schemaStore.schema.project_id}`
})


onMounted(() => {
    schemaStore.model = 'sample'
})

</script>
