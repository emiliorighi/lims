<template>
    <div class="row justify-space-between">
        <div class="flex">
            <div class="row align-center">
                <div class="flex">
                    <h2 class="va-h6">
                        Attributes
                    </h2>
                </div>
                <div class="flex" style="padding-left: 0;">
                    <VaIcon size="large" name="info" color="info" @click="showModal = !showModal">
                    </VaIcon>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInnerLoading :loading="isTsvLoading">
                <VaFileUpload dropZoneText="Drag a TSV file here to import its columns" uploadButtonText="Upload"
                    v-model="tsv" @update:modelValue="parseColumns()" dropzone type="single" file-types=".tsv">
                </VaFileUpload>
            </VaInnerLoading>
        </div>
    </div>
    <div class="row justify-space-between">
        <div class="flex">
            <VaButton @click="deleteRows" preset="primary" color="danger" :disabled="selectedRows.length === 0">Delete
                rows: {{ selectedRows.length }}</VaButton>
        </div>
        <div class="flex">
            <VaButton @click="addAttribute" color="secondary">Add Attribute</VaButton>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <!-- <VaCard>
                <VaCardContent> -->
            <VaDataTable selectable v-model="selectedRows" :items="attributes"
                :columns="['toggle', 'key', 'type', 'description', 'required']">
                <template #header(toggle)>
                </template>
                <template #cell(toggle)="{ row, isExpanded }">
                    <VaButton icon="fa-edit" preset="secondary" @click="row.toggleRowDetails()">
                        Edit
                    </VaButton>
                </template>
                <template #cell(key)="{ rowData }">
                    <VaInput placeholder="Attribute name" v-model="rowData.key"
                        :rules="[(v: string) => v.length > 0, (v: string) => !isDuplicated(v) || 'Name already present']" />
                </template>
                <template #cell(description)="{ rowData }">
                    <VaInput placeholder="Attribute description (optional)" v-model="rowData.description" />
                </template>
                <template #cell(type)="{ rowData, row, isExpanded }">
                    <VaSelect v-model="rowData.type" @update:modelValue="!isExpanded ? row.toggleRowDetails() : ''"
                        :options="['select', 'text', 'date', 'number']">
                        <template #appendInner>
                            <VaChip size="small" v-if="rowData.type === 'select'"
                                :color="rowData.choices?.length ? 'success' : 'danger'">
                                Options: {{ rowData.choices?.length }}
                            </VaChip>
                        </template>
                    </VaSelect>
                </template>
                <template #cell(required)="{ rowData }">
                    <VaCheckbox size="small" v-model="rowData.required"></VaCheckbox>
                </template>
                <template #expandableRow="{ rowData }">
                    <VaCard outlined bordered>
                        <VaCardTitle>
                            {{ rowData.type }}
                        </VaCardTitle>
                        <VaCardContent>
                            <div v-if="rowData.type === 'select'" class="row align-center">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaCheckbox v-model="rowData.multi" label="Multiple Choice">
                                    </VaCheckbox>
                                </div>
                                <div v-if="rowData.fromTSV" class="flex lg12 md12 sm12 xs12">
                                    <VaButton @click="importValues(rowData)">Import Values from TSV
                                    </VaButton>
                                </div>
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaTextarea style="width: 100%;" autosize label="options (One per line)"
                                        :modelValue="rowData.choices?.join('\n')" :rules="[
                                            (v: string) => v.split('\n').filter(t => t).length > 0,
                                            (v: string) => v.split('\n').every(t => t !== '')]"
                                        @update:modelValue="(v: string) => rowData.choices = v.split('\n')">
                                    </VaTextarea>
                                </div>
                            </div>
                            <div v-else class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaInput placeholder="Regex Pattern (optional)" inner-label
                                        v-model="rowData.regex" />
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </template>
            </VaDataTable>
            <!-- </VaCardContent>
            </VaCard> -->
        </div>
    </div>
    <VaModal v-model="showModal">
        <h4 class="va-h4">
            About Attributes
        </h4>
        <p>
            Attributes can be considered as the columns of a tsv or spreasheet.
        </p>
        <h6>
            Types of attributes:
        </h6>
        <ul class="va-unordered">
            <li>Text: a free text field</li>
            <li>Date: a date field</li>
            <li>Number: a number field (decimal or integer)</li>
            <li>Select: a list of choices</li>
        </ul>
    </VaModal>
</template>
<script setup lang="ts">
import { getColumnValues, readTsvHeader } from '../../composables/tsvUtils'
import { onMounted, ref, watch } from 'vue';
import { ResearchFilter } from '../../data/types';
import { useToast } from 'vuestic-ui/web-components';

const props = defineProps<{
    modelAttributes: ResearchFilter[]
}>()

const { init } = useToast()
const showModal = ref(false)
const tsv = ref<undefined | File>()
const isTsvLoading = ref(false)

const attributes = ref<ResearchFilter[]>([])
const emits = defineEmits(['update:modelAttributes'])

const selectedRows = ref<Record<string, any>[]>([])

onMounted(() => attributes.value = [...props.modelAttributes])


function deleteRows() {
    const keys = selectedRows.value.map(({ key }) => key)
    attributes.value = [...attributes.value.filter(({ key }) => !keys.includes(key))]
    selectedRows.value = []
}

// Watch for changes to the local attributes and emit updates.
watch(attributes, (newValue) => {
    //filter out fromTSV key
    const mappedValues = newValue.map((attr) => {
        const { fromTSV, ...otherFields } = attr
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