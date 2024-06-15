<template>
    <VaCard square outlined>
        <VaCardTitle>{{ title }}</VaCardTitle>
        <VaDataTable sticky-header height="500px" :items="items" :columns="columns">
            <template #cell(type)="{ rowData }">
                <va-chip :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
            getFieldType(rowData)
                    }}</va-chip>
            </template>
        </VaDataTable>
    </VaCard>
</template>
<script setup lang="ts">
import { Filter } from '../../../../../data/types';

const props = defineProps<{
    columns: string[],
    items: Filter[],
    title:string
}>()

function getFieldType(item: Filter): 'input' | 'select' | 'range' {
    const filterKeys = Object.keys(item.filter)
    if (filterKeys.includes('input_type')) return 'input'
    if (filterKeys.includes('choices')) return 'select'
    return 'range'
}
const fieldTypesInfo = [
    {
        type: 'input',
        description: 'Input field, used to define input types such as text, date or number',
        color: 'primary'
    },
    {
        type: 'select',
        description: 'Select field, used to define single or a multiple options',
        color: 'secondary'
    },
    {
        type: 'range',
        description: 'Range field, used to define a range of values with one unit',
        color: 'info'
    }
]

</script>