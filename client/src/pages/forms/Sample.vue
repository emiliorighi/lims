<template>
    <div class="row">
        <!-- <div class="flex lg12 md12 sm12 xs12">
            <va-button @click="schemaStore.resetSchema()" round icon="close">{{
                schemaStore.schema.id }}</va-button>
        </div> -->
        <SearchForm :filters="filters" :search-form="{}"></SearchForm>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store'
import { useSampleStore } from '../../stores/sample-store'
import SearchForm from '../../components/forms/SearchForm.vue'
import { ref } from 'vue'
import { useFilters } from './filters'

const samplePayload = ref<Record<string, any>>()
const sample = useSampleStore().sample
const schemaStore = useSchemaStore()

const filters = useFilters(schemaStore.schema)
console.log(filters)
</script>