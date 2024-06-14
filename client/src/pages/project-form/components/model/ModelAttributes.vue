<template>
    <VaCard>
        <VaCardContent class="va-h4">
            Model Attributes
        </VaCardContent>
        <VaCardContent class="va-text-secondary">
            Create a list of attributes that will be used to define samples and experiments. Optionally, upload a tsv
            file to generate the list of attributes
        </VaCardContent>
        <VaDivider />
        <VaCardContent class="row">
            <VaCard :loading="isLoading" class="flex lg12 md12 sm12 xs12" square outlined>
                <VaCardTitle>Attributes list</VaCardTitle>
                <VaCardContent class="row justify-space-between align-center">
                    <div class="flex">
                        Create attributes or upload them from a TSV file
                    </div>
                    <div class="flex">
                        <div class="row">
                            <div class="flex">
                                <VaFileUpload style="z-index: 0" :color="errorMessage ? 'danger' : 'primary'"
                                    v-model="tsv" file-types=".tsv" type="single" undo uploadButtonText="Upload TSV" />
                            </div>
                            <div class="flex">
                                <VaCounter v-model="treshold" :min="0" :max="100" :step="5"
                                    messages="-100 to 100 with step=10" />

                            </div>
                        </div>

                    </div>
                </VaCardContent>
                <VaDataTable :loading="isLoading" sticky-header height="500px" :items="attributeStore.attributes"
                    :columns="columns">
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
                </VaDataTable>
            </VaCard>
            <div class="flex lg6 md6 sm12 xs12">
                <VaCard square outlined>
                    <VaCardTitle>Sample Attributes</VaCardTitle>
                    <VaDataTable sticky-header height="250px" :items="sampleAttributes" :columns="modelColumns">
                        <template #cell(type)="{ rowData }">
                            <va-chip :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
                getFieldType(rowData)
            }}</va-chip>
                        </template>
                    </VaDataTable>
                </VaCard>
                <VaCard square outlined>
                    <VaCardTitle>Experiment Attributes</VaCardTitle>
                    <VaDataTable sticky-header height="250px" :items="experimentAttributes" :columns="modelColumns">
                        <template #cell(type)="{ rowData }">
                            <va-chip :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
                getFieldType(rowData)
            }}</va-chip>
                        </template>
                    </VaDataTable>
                </VaCard>
            </div>
            <VaSplit class="split-demo">
                <template #start>
                    <VaCard square outlined>
                        <VaCardTitle>Attributes list</VaCardTitle>
                        <VaCardContent>Create attributes or upload them from a TSV file
                        </VaCardContent>
                        <VaPopover message="Infer attributes from tsv file">
                            <VaCardActions>
                                <va-file-upload style="z-index: 0" :color="errorMessage ? 'danger' : 'primary'"
                                    v-model="tsv" file-types=".tsv" type="single" undo dropzone
                                    uploadButtonText="Upload TSV" />
                            </VaCardActions>
                        </VaPopover>
                        <VaDataTable :loading="isLoading" sticky-header height="500px"
                            :items="attributeStore.attributes" :columns="columns">
                            <template #header(actions)>
                                <VaButton @click="attributeStore.initAttribute" icon="add">New Attribute</VaButton>
                            </template>
                            <template #cell(type)="{ rowData }">
                                <va-chip
                                    :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
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
                        </VaDataTable>
                    </VaCard>
                </template>
                <template #end>
                    <VaSplit vertical>
                        <template #start>
                            <VaCard square outlined>
                                <VaCardTitle>Sample Attributes</VaCardTitle>
                                <VaDataTable sticky-header height="250px" :items="sampleAttributes"
                                    :columns="modelColumns">
                                    <template #cell(type)="{ rowData }">
                                        <va-chip
                                            :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
                getFieldType(rowData)
            }}</va-chip>
                                    </template>
                                </VaDataTable>
                            </VaCard>
                        </template>
                        <template #end>
                            <VaCard square outlined>
                                <VaCardTitle>Experiment Attributes</VaCardTitle>
                                <VaDataTable sticky-header height="250px" :items="experimentAttributes"
                                    :columns="modelColumns">
                                    <template #cell(type)="{ rowData }">
                                        <va-chip
                                            :color="fieldTypesInfo.filter(f => f.type === getFieldType(rowData))[0].color">{{
                                            getFieldType(rowData)
                                            }}</va-chip>
                                    </template>
                                </VaDataTable>
                            </VaCard>

                        </template>
                    </VaSplit>
                </template>
            </VaSplit>
        </VaCardContent>
    </VaCard>
    <AttributeFormModal />
</template>
<script setup lang="ts">
import { computed, ref, watchEffect, watch, onMounted } from 'vue'
import ProjectService from '../../../../services/clients/ProjectService'
import { Filter } from '../../../../data/types'
import AttributeFormModal from './components/AttributeFormModal.vue'
import { useAttributeStore } from '../../../../stores/attribute-store'
import { useProjectStore } from '../../../../stores/project-store'
import { useToast } from 'vuestic-ui/web-components'

const isLoading = ref(false)
const tsv = ref<undefined | File>()
const errorMessage = ref('')
const columns = [
    { key: "model", sortable: true },
    { key: "key", sortable: true },
    { key: "required", sortable: true },
    { key: "type", width: 120 },
    { key: "actions", width: 80 },
]
const modelColumns = [
    'key', 'required', 'type'
]
const treshold = ref(25)
const attributeStore = useAttributeStore()
const projectStore = useProjectStore()
const { init } = useToast()

watch(() => tsv.value, async () => {
    if (tsv.value) inferAttributes(tsv.value)
})

onMounted(() => {
    const sampleAttrs = projectStore.currentProject.sample.fields.map((f) => { return { model: 'sample', ...f } }) as Filter[]
    const expAttrs = projectStore.currentProject.experiment.fields.map((f) => { return { model: 'experiment', ...f } }) as Filter[]
    //check if project is already uploaded
    attributeStore.attributes = [...sampleAttrs, ...expAttrs]

})

async function inferAttributes(tsv: File) {
    try {
        isLoading.value = !isLoading.value
        const formData = new FormData()
        formData.append('tsv', tsv)
        formData.append('treshold', treshold.value.toString())
        const { data } = await ProjectService.inferAttributesProject(formData)
        attributeStore.attributes = [...attributeStore.attributes, ...data]
    } catch (error) {
        console.error(error)
        init({ message: 'Error inferring attributes from tsv', color: 'danger' })
    } finally {
        isLoading.value = !isLoading.value

    }
}


const sampleAttributes = computed(() => {
    return attributeStore.attributes.filter(a => a.model && a.model === 'sample').map(({ model, ...fields }) => fields)
})
const experimentAttributes = computed(() => {
    return attributeStore.attributes.filter(a => a.model && a.model === 'experiment').map(({ model, ...fields }) => fields)
})

watch(() => [sampleAttributes.value, experimentAttributes.value], () => {
    projectStore.currentProject.sample.fields = sampleAttributes.value
    projectStore.currentProject.experiment.fields = experimentAttributes.value
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

</script>
