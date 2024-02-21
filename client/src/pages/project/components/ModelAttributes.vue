<template>
    <div class="row justify-space-between align-end">
        <div class="flex lg8 md8">
            <h2 class="va-h4">Model Attributes</h2>
            <p>Create a list of attributes that will be used to define samples and experiments. Optionally, upload a tsv
                file to generate the list of attributes</p>
        </div>
        <div class="flex">
            <va-file-upload style="z-index: 0" :color="errorMessage ? 'danger' : 'primary'" v-model="tsv" file-types=".tsv"
                type="single" undo uploadButtonText="Upload TSV" />
        </div>
    </div>
    <VaDivider></VaDivider>
    <div class="row mt-4">
        <div class="flex lg12 md12 sm12 xs12">
            <div class="row justify-space-between align-end">
                <div class="flex lg6 md6">
                    <VaButton :color="projectStore.project.sample.fields.length > 0 ? 'success' : 'danger'">
                        Sample attributes: {{ projectStore.project.sample.fields.length }}
                    </VaButton>
                    <VaButton :color="projectStore.project.experiment.fields.length > 0 ? '#06d6a0' : 'warning'">
                        Experiment attibutes: {{ projectStore.project.experiment.fields.length }}
                    </VaButton>
                    <p class="mt-2" style="color: #e42222" v-if="sampleAttributes.length === 0">Link at least 1 attribute to
                        sample</p>
                </div>
                <div class="flex">
                    <VaPopover v-for="(f, index) in fieldTypesInfo" :key="index" :message="f.description">
                        <va-chip :color="f.color">{{ f.type }}</va-chip>
                    </VaPopover>
                </div>
                <div class="flex lg12 md12 sm12 xs12">
                    <va-data-table :row-bind="isRowBind && getRowBind" sticky-header height="500px"
                        :items="attributeStore.attributes" :columns="columns">
                        <template #header(actions)>
                            <VaButton @click="attributeStore.initAttribute" icon="add">New Attribute</VaButton>
                        </template>
                        <template #cell(type)="{ rowData }">
                            <va-chip :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
                                getFieldType(rowData)
                            }}</va-chip>
                        </template>
                        <template #cell(model)="{ rowData }">
                            <va-select placeholder="Select model" v-model="rowData.model"
                                :options="['sample', 'experiment']"></va-select>
                        </template>
                        <template #cell(actions)="{ rowIndex }">
                            <VaButton preset="plain" icon="edit" @click="editAttribute(rowIndex)" />
                            <VaButton preset="plain" icon="delete" color="danger" class="ml-3"
                                @click="deleteAttribute(rowIndex)" />
                        </template>
                    </va-data-table>
                </div>
            </div>
        </div>
    </div>
    <AttributeFormModal />
</template>
<script setup lang="ts">
import { computed, ref, watchEffect, watch } from 'vue'
import ProjectService from '../../../services/clients/ProjectService'
import { Filter } from '../../../data/types'
import AttributeFormModal from './AttributeFormModal.vue'
import { useAttributeStore } from '../../../stores/attribute-store'
import { useProjectStore } from '../../../stores/project-store'

const tsv = ref<undefined | File>()
const errorMessage = ref('')
const columns = [
    { key: "model", sortable: true },
    { key: "key", sortable: true },
    { key: "required", sortable: true },
    { key: "type", width: 120 },
    { key: "actions", width: 80 },
]
const attributeStore = useAttributeStore()
const isRowBind = ref(true)
const projectStore = useProjectStore()
watchEffect(async () => {
    if (tsv.value) {
        const formData = new FormData()
        formData.append('tsv', tsv.value)
        const { data } = await ProjectService.inferAttributesProject(formData)
        attributeStore.attributes = [attributeStore.attributes, ...data]
    }
})



const sampleAttributes = computed(() => {
    return attributeStore.attributes.filter(a => a.model && a.model === 'sample').map(({model, ...fields}) => fields)
})
const experimentAttributes = computed(() => {
    return attributeStore.attributes.filter(a => a.model && a.model === 'experiment').map(({model, ...fields}) => fields)
})

watch(()=>[sampleAttributes.value, experimentAttributes.value], () => {
    projectStore.project.sample.fields = sampleAttributes.value
    projectStore.project.experiment.fields = experimentAttributes.value
})
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

function getFieldType(item: Filter): 'input' | 'select' | 'range' {
    const filterKeys = Object.keys(item.filter)
    if (filterKeys.includes('input_type')) return 'input'
    if (filterKeys.includes('choices')) return 'select'
    return 'range'
}
function getRowBind(row: Record<string, any>) {
    if (!row.model) return
    const color = row.model === 'sample' ? '#3d9209' : '#06d6a0'
    return {
        style: { 'background-color': color }
    };

}

</script>