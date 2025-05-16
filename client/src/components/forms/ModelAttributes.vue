<template>
    <div v-if="attributes.length === 0" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard stripe stripe-color="danger">
                <VaCardContent>
                    <div class="row align-center">
                        <div class="flex">
                            <VaIcon name="fa-warning" color="danger" />
                        </div>
                        <div class="flex">
                            <h2 class="va-h6">
                                Add at least one attribute before continuing
                            </h2>
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <div v-if="isControlledMode" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard stripe stripe-color="warning">
                <VaCardContent>
                    <div class="row align-center">
                        <div class="flex">
                            <VaIcon name="fa-warning" color="warning" />
                        </div>
                        <div class="flex">
                            <h2 class="va-h6">
                                In controlled mode, only attribute descriptions can be edited
                            </h2>
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <div class="row justify-space-between">
        <div class="flex flex-grow va-text-secondary">
            <VaCard color="backgroundElement">
                <VaCardContent>
                    <span class="va-text-bold">
                        Choose between 4 types of attributes:
                    </span>
                </VaCardContent>
                <VaCardContent>
                    <ul>
                        <li>Text: a free text field</li>
                        <li>Date: a date field of ISO format: YYYY-MM-DD</li>
                        <li>Number: a number field (decimal or integer), english format (decimals separated by .)</li>
                        <li>Select: a list of choices</li>
                    </ul>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <div class="row align-center justify-space-between">
        <div class="flex">
            <h3 class="va-h3">
                Import Attributes
            </h3>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInnerLoading :loading="isTsvLoading">
                <VaFileUpload 
                    :disabled="props.isControlledMode"
                    dropZoneText="Drag a TSV file here to import its columns" 
                    uploadButtonText="Upload"
                    v-model="tsv" 
                    color="primary" 
                    @update:modelValue="parseColumns()" 
                    dropzone 
                    type="single"
                    file-types=".tsv">
                </VaFileUpload>
            </VaInnerLoading>
        </div>
    </div>
    <VaDivider>or</VaDivider>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaButton 
                :disabled="props.isControlledMode"
                icon="fa-plus" 
                block 
                @click="addAttribute">Add a new attribute
            </VaButton>
        </div>
    </div>
    <div v-if="attributes.length" class="row align-end justify-space-between">
        <div class="flex">
            <h3 class="va-h3">Attribute List</h3>
            <p>
                Edit attributes from the table or click on the edit icon to edit the extra informations. Double click on
                the delete icon to delete the
                attribute
            </p>
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <VaDataTable hoverable :items="attributes" no-data-html="Start by adding an attribute"
                :columns="['edit','key', 'type', 'required', 'actions']">
                <template #header(key)>
                    Attribute Name
                </template>
                <template #header(type)>
                    Attribute Type
                </template>
                <template #header(edit)>
                </template>
                <template #header(actions)>
                    <VaButton :disabled="attributes.length === 0 || props.isControlledMode" color="danger"
                        @click="confirmDeleteRows = !confirmDeleteRows">Delete all attributes
                    </VaButton>
                </template>
                <template #cell(edit)="{ row }">
                    <VaButton 
                        @click="row.toggleRowDetails()" 
                        preset="secondary" 
                        icon="fa-edit">
                    </VaButton>
                </template>
                <template #cell(key)="{ rowData }">
                    <VaInput 
                        :disabled="props.isControlledMode"
                        placeholder="Attribute name" 
                        v-model="rowData.key"
                        :rules="[(v: string) => v.length > 0 || 'Name is mandatory', (v: string) => v.toLowerCase() !== 'id' || `${v} is a reserved field, change it`, (v: string) => !isDuplicated(v) || 'Name already present']">
                    </VaInput>
                </template>
                <template #cell(actions)="{ rowIndex }">
                    <VaButton 
                        :disabled="props.isControlledMode"
                        style="margin-left: 10px;" 
                        preset="secondary" 
                        @dblclick="deleteRow(rowIndex)"
                        color="danger" 
                        icon="fa-trash">
                    </VaButton>
                </template>
                <template #cell(type)="{ rowData, isExpanded, row }">
                    <VaSelect 
                        :disabled="props.isControlledMode"
                        v-model="rowData.type" 
                        :options="['select', 'text', 'date', 'number']" 
                        :rules="[(v: any) => {
                            if (v === 'select') {
                                return !rowData.choices || !rowData.choices.length ? 'Add at least 1 options' : true
                            } return true
                        }]" 
                        @update:modelValue="!isExpanded && rowData.type === 'select' ? row.toggleRowDetails() : ''">
                        <template #appendInner>
                            <VaChip size="small" v-if="rowData.type === 'select'"
                                :color="rowData.choices?.length ? 'success' : 'danger'">
                                Options: {{ rowData.choices?.length }}
                            </VaChip>
                        </template>
                    </VaSelect>
                </template>
                <template #cell(required)="{ rowData }">
                    <VaSwitch 
                        :disabled="props.isControlledMode"
                        off-color="backgroundElement" 
                        color="warning" 
                        true-inner-label="Yes"
                        false-inner-label="No" 
                        v-model="rowData.required" 
                    />
                </template>
                <template #expandableRow="{ rowData, toggleRowDetails }">
                    <div class="layout va-gutter-3">
                        <div class="row">
                            <div class="flex lg12 md12 sm12 xs12">
                                <VaCard>
                                    <VaCardContent>
                                        <div class="row justify-space-between">
                                            <div class="flex">
                                                <h4 class="va-h4">Edit Attribute</h4>
                                            </div>
                                            <div class="flex">
                                                <VaButton @click="toggleRowDetails()" color="textPrimary"
                                                    preset="primary">
                                                    Hide form
                                                </VaButton>
                                            </div>
                                        </div>
                                    </VaCardContent>
                                    <VaCardContent>
                                        <div class="row">
                                            <div class="flex lg12 md12 sm12 xs12">
                                                <VaTextarea 
                                                    placeholder="Attribute description (optional)"
                                                    v-model="rowData.description" 
                                                    style="width: 100%;" 
                                                />
                                            </div>
                                        </div>
                                        <div v-if="rowData.type === 'select'" class="row align-center">
                                            <div class="flex lg12 md12 sm12 xs12">
                                                <VaCheckbox 
                                                    :disabled="props.isControlledMode || props.hasRecords"
                                                    v-model="rowData.multi" 
                                                    label="Multiple Choice">
                                                </VaCheckbox>
                                            </div>
                                            <div v-if="rowData.fromTSV" class="flex lg12 md12 sm12 xs12">
                                                <VaButton 
                                                    :disabled="props.isControlledMode || props.hasRecords"
                                                    @click="importValues(rowData)">
                                                    Import Values from TSV
                                                </VaButton>
                                            </div>
                                            <div class="flex lg12 md12 sm12 xs12">
                                                <VaTextarea 
                                                    :disabled="props.isControlledMode || props.hasRecords"
                                                    style="width: 100%;" 
                                                    autosize 
                                                    label="options (One per line)"
                                                    :modelValue="rowData.choices?.join('\n')" 
                                                    :rules="[
                                                        (v: string) => v.split('\n').filter(t => t).length > 0,
                                                        (v: string) => v.split('\n').every(t => t !== '')]"
                                                    @update:modelValue="(v: string) => rowData.choices = v.split('\n')">
                                                </VaTextarea>
                                            </div>
                                        </div>
                                        <div v-else class="row">
                                            <div class="flex lg12 md12 sm12 xs12">
                                                <VaInput 
                                                    :disabled="props.isControlledMode || props.hasRecords"
                                                    placeholder="Regex Pattern (optional)" 
                                                    inner-label
                                                    v-model="rowData.regex" 
                                                />
                                            </div>
                                        </div>
                                    </VaCardContent>
                                </VaCard>
                            </div>
                        </div>
                    </div>
                </template>
            </VaDataTable>
        </div>
    </div>
    <VaModal v-model="confirmDeleteRows" hide-default-actions close-button>
        <h4 class="va-h4">
            Delete all the attributes?
        </h4>
        <template #footer>
            <div class="row justify-space-between">
                <div class="flex">
                    <VaButton color="secondary" @click="confirmDeleteRows = !confirmDeleteRows">Cancel</VaButton>
                </div>
                <div class="flex">
                    <VaButton color="danger" @click="attributes = []; confirmDeleteRows = !confirmDeleteRows">Confirm
                    </VaButton>

                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { getColumnValues, readTsvHeader } from '../../composables/tsvUtils'
import { onMounted, ref, watch } from 'vue';
import { ResearchFilter } from '../../data/types';
import { DataTableRowBind, useToast } from 'vuestic-ui/web-components';

const props = defineProps<{
    modelAttributes: ResearchFilter[]
    isControlledMode?: boolean
    hasRecords?: boolean
}>()

const { init } = useToast()
const showModal = ref(false)
const tsv = ref<undefined | File>()
const isTsvLoading = ref(false)
const confirmDeleteRows = ref(false)
const attributes = ref<ResearchFilter[]>([])
const emits = defineEmits(['update:modelAttributes'])

onMounted(() => attributes.value = [...props.modelAttributes])


function deleteRow(idx: number) {
    attributes.value.splice(idx, 1)
}

// Watch for changes to the local attributes and emit updates.
watch(attributes, (newValue) => {
    //filter out fromTSV key
    const mappedValues = newValue.map((attr) => {
        const { fromTSV, tsvKey, ...otherFields } = attr
        return otherFields
    })

    emits('update:modelAttributes', mappedValues)
}, { deep: true })


const initAttribute: ResearchFilter = {
    type: 'text',
    description: '',
    key: '',
    required: false
}

async function parseColumns() {
    if (tsv.value) {
        const columns = await readTsvHeader(tsv.value)
        const mappedAttributes = columns.map(c => {
            const attr = { ...initAttribute }
            attr.fromTSV = true
            attr.key = c
            attr.tsvKey = c //keep the key to import values
            return attr
        })
        attributes.value.push(...mappedAttributes)
    }
}

function isDuplicated(v: string) {
    return attributes.value.map(({ key }) => key).filter(k => k === v).length > 1
}

function addAttribute() {
    attributes.value.push({ ...initAttribute })
}

async function importValues(attribute: ResearchFilter) {
    if (!tsv.value) return
    try {
        isTsvLoading.value = true
        const { tsvKey, key } = attribute
        const column = tsvKey ?? key
        attribute.choices = await getColumnValues(tsv.value, column)
    } catch (error) {
        init({ message: error as string, color: 'danger' })
    } finally {
        isTsvLoading.value = false

    }

}
</script>
