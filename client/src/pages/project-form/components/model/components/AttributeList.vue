<template>
    <VaDataTable sticky-header height="500px" :items="attributeStore.attributes" :columns="columns">
        <template #header(actions)>
            <VaButton @click="attributeStore.initAttribute" icon="add">New Filter
            </VaButton>
        </template>
        <template #cell(type)="{ rowData }">
            <VaChip :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
        getFieldType(rowData)
    }}</VaChip>
        </template>
        <template #cell(model)="{ rowData }">
            <VaSelect placeholder="Select model" v-model="rowData.model" :options="['sample', 'experiment']"></VaSelect>
        </template>
        <template #cell(actions)="{ rowIndex }">
            <VaButton preset="plain" icon="edit" @click="editAttribute(rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3" @click="deleteAttribute(rowIndex)" />
        </template>
    </VaDataTable>
</template>
<script setup lang="ts">
import { Filter } from '../../../../../data/types';
import { useAttributeStore } from '../../../../../stores/attribute-store'

const attributeStore = useAttributeStore()
const columns = [
    { key: "model", sortable: true },
    { key: "key", sortable: true },
    { key: "required", sortable: true },
    { key: "type", width: 120 },
    { key: "actions", width: 80 },
]

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


function editAttribute(id: number) {
    attributeStore.attributeId = id
    attributeStore.attribute = { ...attributeStore.attributes[id] }
}

function deleteAttribute(id: number) {
    attributeStore.attributes = [...attributeStore.attributes.slice(0, id), ...attributeStore.attributes.slice(id + 1)];
}

</script>