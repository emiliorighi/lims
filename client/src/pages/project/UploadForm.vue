<template>
    <div>
        <div class="row">
            <div class="flex">
                <h1 class="va-h1">Upload Records</h1>
            </div>
        </div>
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <VaForm ref="uploadForm">
                    <VaStepper color="textPrimary" @finish="submit" linear v-model="currentStep" :steps="steps">
                        <template #step-content-0>
                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaSelect placeholder="Select the target model" v-model="selectedModel"
                                        :options="modelNames"
                                        :rules="[(v: any) => !!v || 'Model selection is required']" />
                                </div>

                            </div>
                        </template>
                        <template #step-content-1>
                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaFileUpload
                                        dropZoneText="Drag a TSV file here to map its columns to the model field"
                                        uploadButtonText="Upload" v-model="tsv" @update:modelValue="parseColumns()"
                                        dropzone type="single" file-types=".tsv">
                                    </VaFileUpload>
                                </div>
                                <div class="flex lg6 md6 sm12 xs12">
                                    <VaSelect placeholder="Select the behaviour model" v-model="behaviour"
                                        :options="['SKIP', 'UPDATE']"
                                        :messages="['What to do when encountering an existing record']" />
                                </div>
                                <div class="flex lg6 md6 sm12 xs12">
                                    <VaCounter style="width: 100%;" v-model="header"
                                        :messages="['The 0-based header row position, records will be processed starting by the next row after the header row']">
                                    </VaCounter>
                                </div>
                            </div>
                        </template>
                        <template #step-content-2>
                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaButton @click="assignColumns" color="textPrimary">Auto-Assign Matching
                                        Fields</VaButton>
                                </div>
                                <div class="flex lg12 md12 sm12 xs12">
                                    <div v-for="mappedField in mappedFields" class="row align-center">
                                        <div class="flex lg6 md6 sm12 x12">
                                            <VaInput :model-value="mappedField.field" read-only
                                                :messages="['The field name of the model, can not be edited']">
                                                <template #appendInner>
                                                    <VaChip v-if="mappedField.required" size="small"
                                                        :color="mappedField.column ? 'success' : 'danger'">
                                                        required
                                                    </VaChip>
                                                </template>
                                            </VaInput>
                                        </div>
                                        <div class="flex lg6 md6 sm12 x12">
                                            <VaSelect searchable :options="options" track-by="text" value-by="text"
                                                text-by="text"
                                                :messages="['The incoming TSV column to map agains the field name']"
                                                v-model="mappedField.column" clearable :rules="[
                                                    (v: any) => !(mappedField.required && !v) || 'This field is required'
                                                ]">
                                            </VaSelect>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-if="refModel" class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <h2 class="va-h4">Reference Model Id fields</h2>
                                    <p>Select the list of columns that maps to the refence model id field: {{
                                        refModel.id_format.join('_') }}. The
                                        selection order matters!
                                    </p>
                                </div>
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaSelect placeholder="Reference models columns" multiple :options="options"
                                        v-model="referencModelFields" track-by="text" value-by="text" text-by="text"
                                        :messages="['Choose the columns that combined point to the reference model record']">
                                    </VaSelect>
                                </div>
                            </div>
                        </template>
                    </VaStepper>
                </VaForm>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useSchemaStore } from '../../stores/schema-store';
import { readTsvHeader } from '../../composables/tsvUtils'
import { defineVaStepperSteps, useForm, useToast, VaCounter, VaInput } from 'vuestic-ui';
import AuthService from '../../services/clients/AuthService';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';

const { init } = useToast()
const { validate } = useForm('uploadForm')
const schemaStore = useSchemaStore()
const router = useRouter()
const props = defineProps<{
    projectId: string
}>()
const steps = ref(defineVaStepperSteps([
    {
        label: 'Model Selection',
        beforeLeave: (step) => { step.hasError = !validate() }
    },
    {
        label: 'TSV Upload',
        beforeLeave: (step) => {
            if (!tsv.value) {
                step.hasError = true
                return
            }
            initFields()
        },
    },
    {
        label: 'Columns Mapping',
    }
]))

const isLoading = ref(false)
const tsv = ref<undefined | File>()
const selectedModel = ref(null)
const currentStep = ref(0)
const header = ref(0)
const behaviour = ref('SKIP')
const referencModelFields = ref<string[]>([])
const models = computed(() => schemaStore.schema?.models ?? [])
const modelNames = computed(() => models.value.map(({ name }) => name) ?? [])
const refModelName = computed(() => schemaStore.schema?.models.find(m => m.name === selectedModel.value)?.reference_model)
const refModel = computed(() => schemaStore.schema?.models.find(m => m.name === refModelName.value))

const modelFields = computed(() => models.value.find(({ name }) => name === selectedModel.value)?.fields ?? [])

const modelFieldsKeys = computed(() => modelFields.value.map(({ key }) => key))

const mappedFields = ref<{ field: string, column: string | null, required: boolean }[]>([])

const tsvColumns = ref<string[]>([])

const options = computed(() => {
    const fields = mappedFields.value.map(({ column }) => column).filter(c => !!c)
    return tsvColumns.value.map(c => ({ text: c, disabled: fields.includes(c) }))
})


async function submit() {
    if (!validate()) return
    if (!tsv.value || !selectedModel.value) return
    const map = mappedFields.value.filter(({ column }) => !!column).map(({ field, column }) => [field, column])
    const formData = new FormData()
    formData.append('file', tsv.value)
    formData.append('map', JSON.stringify(Object.fromEntries(map)))
    formData.append('referenceFields', JSON.stringify(referencModelFields.value))
    formData.append('model', selectedModel.value)
    formData.append('behaviour', behaviour.value)
    formData.append('header', header.value.toString())
    let success = false
    try {
        isLoading.value = true
        const { data } = await AuthService.uploadTSV(props.projectId, formData)
        init({ color: 'success', message: data })
        success = true
    } catch (error) {
        const err = error as AxiosError
        success = false
        let message = err.message
        const respData = err.response?.data as any
        if (respData) {
            message = respData.message ? respData.message : respData
        }
        init({ color: 'danger', message: message, closeable: true, duration: 100000 })
    } finally {
        isLoading.value = false
        if (success) router.push({ name: 'projectModel', params: { projectId: props.projectId, modelName: selectedModel.value } })
    }
}
function initFields() {
    mappedFields.value = [
        ...modelFields.value.map(modelField => ({ field: modelField.key, column: null, required: modelField.required }))
    ]
    referencModelFields.value = []
}
//overwrite current assigned values and find potential matches
function assignColumns() {

    const matches = matchAndRemove(modelFieldsKeys.value, tsvColumns.value)
    mappedFields.value = [
        ...mappedFields.value.map(({ field, column, required }) => {
            const match = matches[field]
            if (match) {
                return { field, column: match, required }
            }
            return { field, column, required }
        })
    ]
}

async function parseColumns() {
    if (tsv.value) {
        try {
            const columns = await readTsvHeader(tsv.value)
            tsvColumns.value = [...columns]
        } catch (error) {
            init({ color: 'danger', message: error as string })
        }
    }
}

function matchAndRemove(listA: string[], listB: string[]): Record<string, string | null> {
    const result: Record<string, string | null> = {};
    const remainingB = new Map<string, string>(); // Stores lowercase -> original values

    // Populate map with lowercase keys for case-insensitive lookup
    for (const b of listB) {
        remainingB.set(b.toLowerCase(), b);
    }

    // Step 1: Exact matches (case-insensitive)
    for (const a of listA) {
        const aLower = a.toLowerCase();
        if (remainingB.has(aLower)) {
            result[a] = remainingB.get(aLower) || null; // Store original case value
            remainingB.delete(aLower);
        } else {
            result[a] = null; // Initialize with null in case no match is found
        }
    }

    // Step 2: Partial matches (case-insensitive)
    for (const a of listA) {
        if (result[a] === null) {
            const aLower = a.toLowerCase();
            for (const [bLower, bOriginal] of Array.from(remainingB.entries())) {
                if (bLower.includes(aLower) || aLower.includes(bLower)) {
                    result[a] = bOriginal;
                    remainingB.delete(bLower);
                    break;
                }
            }
        }
    }

    return result;
}

</script>