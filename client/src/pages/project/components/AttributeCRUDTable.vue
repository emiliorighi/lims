<template>
    <VaDataTable class="table-crud" v-model="project[model].id_format" :items="project[model].fields" :columns="columns"
        striped selectable select-mode="multiple" items-track-by="key">
        <template #cell(type)="{ rowData }">
            <va-chip color="info">{{ getFieldType(rowData) }}</va-chip>
        </template>
    </VaDataTable>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../../stores/project-store'
import { Filter } from '../../../data/types'
import AttributeFormModal from './AttributeFormModal.vue'

const props = defineProps<{
    model: 'sample' | 'experiment'
}>()

const { project } = useProjectStore()

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
</script>
<style lang="scss" scoped>
.table-crud {
    --va-form-element-default-width: 0;

    .VaInput {
        display: block;
    }

    &__slot {
        th {
            vertical-align: middle;
        }
    }
}
</style>