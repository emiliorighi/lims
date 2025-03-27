<template>
    <div class="row">
        <div v-for="filter in queryFilters" class="flex lg12 md12 sm12 xs12">
            <FilterField :key="filter.key" @update-query="handleUpdate" :field="filter" :project-id="projectId"
                :model-name="model.name">
            </FilterField>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useRecordStore } from '../../../stores/record-store';
import { ReseachModel } from '../../../data/types';
import FilterField from '../../../components/filters/FilterField.vue';

const props = defineProps<{
    projectId: string,
    model: ReseachModel
}>()

const recordStore = useRecordStore()

async function handleUpdate(payload: { key: string, query: Record<string, any> }) {
    const { key, query } = payload
    recordStore.searchForm[key] = { ...query }
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

const queryFilters = computed(() => props.model.fields.map(({ key, type }) => {
    let payload = type === 'date' || type === 'number' ? { [key]: null } : { [`${key}__in`]: null }
    if (recordStore.searchForm[key]) {
        payload = recordStore.searchForm[key]
    }
    return { key, type, payload }
}))


</script>
