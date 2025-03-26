<template>
    <div class="row justify-space-between">
        <div class="flex lg8 md8">
            <div class="row">
                <div class="flex lg8 md8">
                    <DebounceInput placeholder="Search by ID" @input="recordStore.showFilters = false" icon="fa-search"
                        :parent-model="filter" @change="handleSearch" :clearable="true" />
                </div>
                <div class="flex">
                    <VaButton style="margin-left: 3px;" preset="primary" color="textPrimary" icon="help"
                        @click="showQueryInfo = !showQueryInfo" />
                </div>
            </div>
        </div>
        <div class="flex">
            <VaButton color="textPrimary" preset="primary" @click="recordStore.showFilters = !recordStore.showFilters"
                :icon="recordStore.showFilters ? 'fa-filter-circle-xmark' : 'fa-filter'"> Filters
            </VaButton>
        </div>
    </div>
    <VaModal v-model="showQueryInfo">
        <template #header>
            <h3 class="va-h3">
                Record identifier filter
            </h3>
            <p class="va-text-secondary">This input filters by the formatted identifier of {{ model.name }} that is
                composed by
                the
                following fields:</p>
        </template>
        <div class="layout va-gutter-3 fluid">
            <div class="row">
                <div v-for="idField in model.id_format" :key="idField" class="flex">
                    <VaChip color="textPrimary">{{ idField }}</VaChip>
                </div>
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRecordStore } from '../../../stores/record-store';
import { ReseachModel } from '../../../data/types';
import DebounceInput from '../../../components/inputs/DebounceInput.vue';

const props = defineProps<{
    projectId: string,
    model: ReseachModel
}>()

const emits = defineEmits(['search'])

const recordStore = useRecordStore()
const showQueryInfo = ref(false)

const filter = computed(() => recordStore.searchForm.filter ? recordStore.searchForm.filter?.filter : "")

async function handleSearch(filter: string) {
    recordStore.searchForm.filter = { filter }
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

</script>