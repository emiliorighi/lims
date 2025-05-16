<template>
    <VaModal close-button hide-default-actions v-model="recordStore.showTSVImportModal">
        <template #header>
            <div class="row align-center justify-space-between">
                <div class="flex">
                    <h3 class="va-h3">
                        Import Records
                    </h3>
                    <p class="va-text-secondary">Import records from a TSV file</p>
                </div>
                <VaIcon color="textPrimary" size="large" class="flex" name="fa-file-import" />
            </div>
        </template>
        <div class="layout fluid va-gutter-5">
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaForm :key="modelName" ref="uploadForm">
                        <VaInnerLoading :loading="isLoading">
                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaFileUpload :color="tsv ? 'textPrimary' : 'danger'"
                                        dropZoneText="Drag a TSV file here to map its columns to the model field"
                                        uploadButtonText="Upload" v-model="tsv" @update:modelValue="parseColumns()"
                                        dropzone type="single" file-types=".tsv">
                                    </VaFileUpload>
                                </div>
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaSelect placeholder="Select the behaviour model" v-model="behaviour"
                                        :options="['SKIP', 'UPDATE']"
                                        :messages="['Select how existing records should be handled during TSV import: SKIP to ignore them, or UPDATE to overwrite them with new data.']" />
                                </div>
                            </div>
                            <div v-if="tsv" class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaButton block @click="assignColumns" color="textPrimary">Auto-Assign
                                        Matching
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
                                    <p>Select the list of columns that maps to the refence model id field:
                                        {{
                                            refModel.id_format.join('_') }}. The
                                        selection order matters!
                                    </p>
                                </div>
                                <div class="flex lg12 md12 sm12 xs12">
                                    <VaSelect placeholder="Reference models columns" multiple :options="options"
                                        v-model="referencModelFields" track-by="text" value-by="text" text-by="text"
                                        :messages="['Choose the columns that combined point to the reference model record']"
                                        :rules="[(v: any) => (v && v.length > 0) || 'Select at least one field']">
                                    </VaSelect>
                                </div>
                            </div>
                        </VaInnerLoading>
                    </VaForm>
                </div>
            </div>
        </div>
        <template #footer>
            <VaButton :loading="isLoading" @click="submit"> Submit </VaButton>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { readTsvHeader } from '../../composables/tsvUtils'
import { useForm, useToast, VaInnerLoading, VaInput } from 'vuestic-ui';
import AuthService from '../../services/clients/AuthService';
import { AxiosError } from 'axios';
import { ResearchModel } from '../../data/types';
import { useRecordStore } from '../../stores/record-store';
import { useModelStore } from '../../stores/model-store';

const { init } = useToast()
const { validate } = useForm('uploadForm')
const props = defineProps<{
    projectId: string
    modelName: string,
    refModel?: ResearchModel | null,
}>()

const recordStore = useRecordStore()
const modelStore = useModelStore()
const isLoading = ref(false)
const tsv = ref<undefined | File>()
const behaviour = ref('SKIP')
const referencModelFields = ref<string[]>([])

const modelFields = computed(() => modelStore.filters)

const modelFieldsKeys = computed(() => modelFields.value.map(({ key }) => key))

const mappedFields = ref<{ field: string, column: string | null, required: boolean }[]>([])

const tsvColumns = ref<string[]>([])

const options = computed(() => {
    const fields = mappedFields.value.map(({ column }) => column).filter(c => !!c)
    return tsvColumns.value.map(c => ({ text: c, disabled: fields.includes(c) }))
})


async function submit() {
    if (!validate() || !tsv.value) {
        init({ color: 'danger', message: 'Fill the required fields first' })
        return
    }
    const map = mappedFields.value.filter(({ column }) => !!column).map(({ field, column }) => [field, column])
    const formData = new FormData()
    formData.append('file', tsv.value)
    formData.append('map', JSON.stringify(Object.fromEntries(map)))
    formData.append('referenceFields', JSON.stringify(referencModelFields.value))
    formData.append('model', props.modelName)
    formData.append('behaviour', behaviour.value)
    let success = false
    try {
        isLoading.value = true
        const { data } = await AuthService.uploadTSV(props.projectId, props.modelName, formData)
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
        if (success) {
            recordStore.resetPagination()
            recordStore.resetSearchForm()
            await recordStore.fetchRecords(props.projectId, props.modelName)
            await modelStore.getStats(props.projectId, props.modelName)
            recordStore.showTSVImportModal = false
        }
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
            initFields()
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