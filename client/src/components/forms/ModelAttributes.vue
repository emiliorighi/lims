<template>
    <VaCard>
        <VaCardContent>
            <div class="row mb-4">
                <div class="flex">
                    <h2 class="va-h3">
                        Model Attributes
                    </h2>
                    <p class="va-text-secondary">
                        Define the attributes (fields) for your model. You can add them manually or import from
                        a TSV file. </p>
                </div>
            </div>
            <div v-if="attributes.length === 0" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard message="Add at least one attribute before continuing" icon="fa-warning"
                        color="danger" />

                </div>
            </div>
            <div v-if="isControlledMode" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard message="In controlled mode, only attribute descriptions can be edited" icon="fa-warning"
                        color="warning" />
                </div>
            </div>
            <div class="row justify-space-between">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard color="backgroundElement">
                        <VaCardContent>
                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <h3 class="va-h6">Available Attribute Types</h3>
                                </div>
                            </div>
                            <div class="row row-equal">
                                <div v-for="type in attributeTypes" :key="type.id" class="flex lg6 md6 sm12 xs12">
                                    <VaCard>
                                        <VaCardContent>
                                            <div class="row align-center">
                                                <div class="flex">
                                                    <VaIcon :name="type.icon" :color="type.color" />
                                                </div>
                                                <div class="flex">
                                                    <h4 class="va-h6">{{ type.name }}</h4>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="flex">
                                                    <p class="va-text-secondary">
                                                        {{ type.description }}
                                                    </p>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="flex lg12 md12 sm12 xs12">
                                                    <div class="example-box">
                                                        <p class="va-text-secondary mb-2">Example:</p>
                                                        <VaChip v-for="example in type.examples" :key="example"
                                                            :color="type.color" size="small" class="mr-2">
                                                            {{ example }}
                                                        </VaChip>
                                                    </div>
                                                </div>
                                            </div>
                                        </VaCardContent>
                                    </VaCard>
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>
            <div class="row">
                <div class="flex">
                    <h3 class="va-h6">
                        Import from TSV File
                    </h3>
                    <p class="va-text-secondary">
                        Upload a TSV file to automatically create attributes from its columns, you can then edit
                        the attributes as you want.
                    </p>
                </div>
            </div>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaInnerLoading :loading="isTsvLoading">
                        <VaFileUpload :disabled="isControlledMode" style="height:200px;align-content:center"
                            dropZoneText="Drag a TSV file here to import its columns" uploadButtonText="Upload"
                            v-model="tsv" color="primary" @update:modelValue="parseColumns()" dropzone type="single"
                            file-types=".tsv">
                        </VaFileUpload>
                    </VaInnerLoading>
                </div>
            </div>
            <VaDivider />
            <div class="row align-end justify-space-between">
                <div class="flex">
                    <h3 class="va-h6">Attribute List ({{ attributes.length }})</h3>
                    <p class="va-text-secondary">
                        Edit attributes from the table or click on the edit icon to edit the extra informations.
                    </p>
                    <p class="va-text-secondary"> <span class="va-text-bold"> Double click </span> on the
                        delete icon to delete an attribute
                    </p>
                </div>
                <div class="flex">
                    <VaButton size="large" :disabled="isControlledMode" icon="fa-plus" @click="addAttribute">Add
                        attribute
                    </VaButton>
                </div>
            </div>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaDataTable hoverable :items="attributes" no-data-html="Start by adding an attribute"
                        :columns="['edit', 'key', 'type', 'required', 'actions']">
                        <template #header(key)>
                            Attribute Name
                        </template>
                        <template #header(type)>
                            Attribute Type
                        </template>
                        <template #header(edit)>
                        </template>
                        <template #header(actions)>
                        </template>
                        <template #cell(edit)="{ row }">
                            <VaButton @click="row.toggleRowDetails()" preset="secondary" icon="fa-edit">
                            </VaButton>
                        </template>
                        <template #cell(key)="{ rowData }">
                            <VaInput :disabled="isControlledMode" placeholder="Attribute name" v-model="rowData.key"
                                :rules="[(v: string) => v.length > 0 || 'Name is mandatory', (v: string) => v.toLowerCase() !== 'id' || `${v} is a reserved field, change it`, (v: string) => !isDuplicated(v) || 'Name already present']">
                            </VaInput>
                        </template>
                        <template #cell(actions)="{ rowIndex }">
                            <VaButton :disabled="isControlledMode" style="margin-left: 10px;" preset="secondary"
                                @dblclick="deleteRow(rowIndex)" color="danger" icon="fa-trash">
                            </VaButton>
                        </template>
                        <template #cell(type)="{ rowData, isExpanded, row }">
                            <VaSelect :disabled="isControlledMode" v-model="rowData.type"
                                :options="['select', 'text', 'date', 'number']" :rules="[(v: any) => {
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
                            <VaSwitch :disabled="isControlledMode" off-color="backgroundElement" color="warning"
                                true-inner-label="Yes" false-inner-label="No" v-model="rowData.required" />
                        </template>
                        <template #expandableRow="{ rowData, toggleRowDetails }">
                            <div class="layout va-gutter-3">
                                <div class="row">
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <VaCard>
                                            <VaCardContent>
                                                <div class="row justify-space-between">
                                                    <div class="flex">
                                                        <p class="va-text-bold">Edit Attribute</p>
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
                                                        <VaTextarea placeholder="Attribute description (optional)"
                                                            v-model="rowData.description" style="width: 100%;" />
                                                    </div>
                                                </div>
                                                <div v-if="rowData.type === 'select'" class="row align-center">
                                                    <div class="flex lg12 md12 sm12 xs12">
                                                        <VaCheckbox :disabled="isControlledMode" v-model="rowData.multi"
                                                            label="Multiple Choice">
                                                        </VaCheckbox>
                                                    </div>
                                                    <div v-if="rowData.fromTSV" class="flex lg12 md12 sm12 xs12">
                                                        <VaButton :disabled="isControlledMode"
                                                            @click="importValues(rowData)">
                                                            Import Values from TSV
                                                        </VaButton>
                                                    </div>
                                                    <div class="flex lg12 md12 sm12 xs12">
                                                        <VaTextarea :disabled="isControlledMode" style="width: 100%;"
                                                            autosize label="options (One per line)"
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
                                                        <VaInput :disabled="isControlledMode"
                                                            placeholder="Regex Pattern (optional)" inner-label
                                                            v-model="rowData.regex" />
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
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { getColumnValues, readTsvHeader } from '../../composables/tsvUtils'
import { onMounted, ref, watch } from 'vue';
import { ResearchFilter } from '../../data/types';
import { useToast } from 'vuestic-ui/web-components';
import AlertCard from '../cards/AlertCard.vue';

const props = defineProps<{
    modelAttributes: ResearchFilter[]
    isControlledMode?: boolean
}>()

const initAttribute: ResearchFilter = {
    type: 'text',
    description: '',
    choices: [],
    key: '',
    required: false
}


const { init } = useToast()
const tsv = ref<undefined | File>()
const isTsvLoading = ref(false)

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

const attributeTypes = [
    {
        id: 'text',
        name: 'Text',
        icon: 'fa-font',
        color: 'primary',
        description: 'A free text field for storing any string value. Use this for names, descriptions, or any other text-based information.',
        examples: ['Sample Name', 'Description text']
    },
    {
        id: 'date',
        name: 'Date',
        icon: 'fa-calendar',
        color: 'success',
        description: 'A date field that follows the ISO format (YYYY-MM-DD). Perfect for recording dates of experiments, samples, or events.',
        examples: ['2024-03-20', '2024-12-31']
    },
    {
        id: 'number',
        name: 'Number',
        icon: 'fa-hashtag',
        color: 'warning',
        description: 'A numeric field that accepts both integers and decimals. Uses English format with decimal points (.). Ideal for measurements, counts, or any numerical data.',
        examples: ['42', '3.14159']
    },
    {
        id: 'select',
        name: 'Select',
        icon: 'fa-list',
        color: 'info',
        description: 'A dropdown field with predefined choices. Use this when you need to restrict input to specific options or categories.',
        examples: ['Option A', 'Option B', 'Option C']
    }
]
</script>

<style scoped>
.example-box {
    background-color: var(--va-background-element);
    padding: 0.75rem;
    border-radius: 4px;
}

.example-box .va-chip {
    margin-right: 0.5rem;
}
</style>
