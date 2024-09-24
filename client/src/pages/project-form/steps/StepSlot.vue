<template>
    <div class="step-slot">
        <h4 class="va-h4"> ID mapping of {{ model }}
        </h4>
        <p class="va-text-secondary"> Select at least one filter key that will be used to generate the id</p>
        <div class="row align-center">
            <div class="flex">
                <span class="va-text-success" v-if="modelId.length"><b>{{ currentProject[model].id_format.join('_') }}</b></span>
                <span v-else class="va-text-danger"><b>Select at least one field!</b></span>
            </div>
        </div>
        <VaAlert v-if="currentProject[model].fields.length === 0" color="warning">
            Any experiment field declared, skip this step!
        </VaAlert>
        <VaDataTable v-model="currentProject[model].id_format" :items="currentProject[model].fields" :columns="columns"
            striped selectable select-mode="multiple" items-track-by="key">
            <template #cell(type)="{ rowData }">
                <va-chip color="info">{{ getFieldType(rowData) }}</va-chip>
            </template>
        </VaDataTable>
    </div>
</template>
<script setup lang="ts">
import { ModelType, Filter } from '../../../data/types'
import { computed } from 'vue';
import { useProjectStore } from '.././../../stores/project-store';

const { currentProject } = useProjectStore()
const props = defineProps<{
    model: ModelType
}>()

const columns = [
    { key: "key", sortable: true },
    { key: "label", sortable: true },
    { key: "description", sortable: true },
    { key: "required", sortable: true },
    { key: "type", width: 120 },
];

function getFieldType(item: Filter): 'input' | 'select' | 'range' {
    const filterKeys = Object.keys(item.filter)
    if (filterKeys.includes('input_type')) return 'input'
    if (filterKeys.includes('choices')) return 'select'
    return 'range'
}

const modelId = computed(() => {
    return currentProject[props.model].id_format
})

</script>
