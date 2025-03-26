<template>
    <VaCollapse v-model="recordStore.showFilters">
        <template #header>
            <span></span>
        </template>
        <template #body>
            <VaCardContent>
                <div class="row align-center justify-space-between">
                    <div class="flex">
                        <h2 class="va-h6">
                            Filters
                        </h2>
                    </div>
                </div>
                <div class="row">
                    <div v-for="field in model.fields" :key="field.key" class="flex lg4 md4 sm12 xs12">
                        <VaButtonDropdown :label="field.key" color="textPrimary"
                            :preset="activeFiltersKeys.includes(field.key) ? undefined : 'primary'">
                        
                        </VaButtonDropdown>
                        <!-- <FilterField :key="field.key" @update-query="handleUpdate" :field="field"
                            :project-id="projectId" :model-name="model.name" :query="recordStore.searchForm[field.key]">
                        </FilterField> -->
                    </div>
                </div>
                <div class="row justify-space-between">
                    <div class="flex">
                        <VaButton @click="handleReset" color="danger">Reset Filters</VaButton>
                    </div>
                    <div class="flex">
                        <VaButton :disabled="activeFilters.length === 0" @click="submitFilters" color="textPrimary">
                            Apply Filters</VaButton>
                    </div>

                </div>
            </VaCardContent>
        </template>
    </VaCollapse>
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

const activeFiltersKeys = computed(() => Object.keys(recordStore.searchForm))

const activeFilters = computed(() => Object.values(recordStore.searchForm).map(value => Object.values(value)).flat().filter(v => v))

function handleUpdate(payload: { key: string, query: Record<string, any> }) {
    const { key, query } = payload
    recordStore.searchForm[key] = { ...query }
}


async function handleReset() {
    recordStore.resetSearchForm()
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

async function submitFilters() {
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}


</script>
