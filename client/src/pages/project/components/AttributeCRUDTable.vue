<template>
    <VaDataTable class="table-crud" v-model="project[model].id_format" :items="project[model].fields" :columns="columns"
        striped selectable select-mode="multiple" items-track-by="key">
        <template #headerAppend>
            <tr class="table-crud__slot">
                <th></th>
                <th v-for="c in columns" class="p-1">
                    <VaButton block v-if="c.key === 'actions'" :round="false" @click="attributeStore.initAttribute()"
                        icon="add">
                        New Item</VaButton>
                </th>
            </tr>
        </template>
        <template #cell(type)="{ rowData }">
            <va-chip color="info">{{ getFieldType(rowData) }}</va-chip>
        </template>
        <template #cell(actions)="{ rowIndex }">
            <VaButton preset="plain" icon="edit" @click="editAttribute(rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3" @click="deleteAttribute(rowIndex)" />
        </template>
    </VaDataTable>
    <AttributeFormModal  :model="model" />
</template>
<script setup lang="ts">
import { useProjectStore } from '../../../stores/project-store'
import { useAttributeStore } from '../../../stores/attribute-store'
import { Filter } from '../../../data/types'
import AttributeFormModal from './AttributeFormModal.vue'

const props = defineProps<{
    model: 'sample' | 'experiment'
}>()

const attributeStore = useAttributeStore()
const { project } = useProjectStore()

const columns = [
    { key: "key", sortable: true },
    { key: "label", sortable: true },
    { key: "description", sortable: true },
    { key: "required", sortable: true },
    { key: "type", width: 120 },
    { key: "actions", width: 80 },
];

function editAttribute(id: number) {
    attributeStore.attributeId = id
    attributeStore.attribute = { ...project[props.model].fields[id] }
}
function deleteAttribute(id: number) {
    project[props.model].fields = [...project[props.model].fields.slice(0, id), ...project[props.model].fields.slice(id + 1)];
}
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