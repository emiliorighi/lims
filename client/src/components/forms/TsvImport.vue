<template>
    <div class="row justify-center">
        <div class="flex lg12 md12 sm12 xs12">
            <va-card>
                <va-card-title>
                    TSV import
                </va-card-title>
                <va-card-content>
                    <va-form tag="form">
                        <va-stepper @finish="submitTsv" linear v-model="currentStep" :steps="steps">
                            <template #step-content-0>
                                <h2 class="va-h2">
                                    TSV Upload
                                </h2>
                                <p>Upload a valid TSV file!</p>
                                <div class="row justify-center">
                                    <div class="flex">
                                        <va-file-upload dropzone dropzone-text="Upload a TSV file" v-model="tsv"
                                            file-types=".tsv" type="single" undo>
                                        </va-file-upload>
                                    </div>
                                </div>
                                <div v-if="rows.length" class="row">
                                    <va-alert color="danger" v-if="headerError">Header length is less then first row length|</va-alert>
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <va-data-table sticky-header :items="rows" :columns="header">

                                        </va-data-table>
                                    </div>
                                </div>
                            </template>
                            <template #step-content-1>
                                <h2 class="va-h2">
                                    Header Mapping
                                </h2>
                                <p>Drag and Drop a header column to the desired target field</p>
                                <div class="row">
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <va-data-table sticky-header :items="rows" :columns="header">

                                        </va-data-table>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="flex lg6 md6 sm12 xs12">
                                        <h4 class="va-h4">
                                            Header Columns
                                        </h4>
                                        <va-divider></va-divider>
                                        <div class="row">
                                            <div class="flex">
                                                <va-chip style="margin: 0.2rem;" v-for="h in header" :key="h"
                                                    draggable="true" v-on:dragstart="handleDragStart($event, h)">{{ h
                                                    }}</va-chip>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex lg6 md6 sm12 xs12">
                                        <h4 class="va-h4">
                                            Target Fields
                                        </h4>
                                        <va-divider></va-divider>
                                        <div class="row">
                                            <div class="flex lg12 md12 sm12 xs12" v-for="item in fields" :key="item.key"
                                                v-on:dragover.prevent v-on:drop="handleDrop($event, item.key)">
                                                <va-card
                                                    :color="item.required ? mappedFields[item.key] ? 'success' : 'danger' : 'secondary'">
                                                    <va-card-title>{{ item.key }}</va-card-title>
                                                    <va-card-content v-if="item.required">This field is
                                                        required</va-card-content>
                                                    <va-card-content v-if="mappedFields[item.key]">
                                                        <va-chip>{{ mappedFields[item.key] }}</va-chip> <va-icon
                                                            @click="mappedFields[item.key] = ''" name="remove"></va-icon>
                                                        <!-- <p>Preview: {{ rows[0][mappedFields[item.key]] }}</p> -->
                                                    </va-card-content>
                                                </va-card>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <p></p>
                            </template>
                            <template #step-content-2>
                            </template>
                        </va-stepper>
                    </va-form>
                </va-card-content>
            </va-card>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watchEffect } from 'vue'
import { useSchemaStore } from '../../stores/schema-store'
import { defineVaStepperSteps } from 'vuestic-ui'
import SampleService from '../../services/clients/SampleService'
import { AxiosError } from 'axios'
import { useGlobalStore } from '../../stores/global-store'

const { toast } = useGlobalStore()
const isLoading = ref(false)
const { project_id, sample } = useSchemaStore().schema
const { fields } = sample
const tsv = ref<undefined | File>()
const errors = ref<Record<string, any>[]>([])
const headerError = ref(false)
const header = ref<string[]>([])
const rows = ref<Record<string, string>[]>([])
const mappedFields = ref<Record<string, string>>({})
const currentStep = ref(0)
const steps = ref(defineVaStepperSteps([
    {
        label: 'TSV Upload', beforeLeave: (step) => { step.hasError = !tsv.value }
    },
    {
        label: 'Fields mapping', beforeLeave: (step) => { step.hasError = !requiredFieldsFilled.value }
    },
    {
        label: 'Data submission'
    }
]))

watchEffect(() => {
    if (tsv.value) {
        parseHeader(tsv.value)
    } else {
        header.value = []
        mappedFields.value = {}
    }
})

const requiredFieldsFilled = computed(() => {
    return fields.filter(f => f.required).map(f => f.key).every(f => Object.keys(mappedFields.value).includes(f) && mappedFields.value[f])
})

async function submitTsv() {

    const formData = new FormData()
    if (tsv.value) formData.append('sample_tsv', tsv.value)
    Object.entries(mappedFields.value).forEach(([k, v]) => {
        formData.append(k, v)
    })
    try {
        const { data } = await SampleService.uploadSampleTSV(project_id, formData)
    } catch (e) {
        const axiosError = e as AxiosError
        console.log(axiosError.message)
    } finally {

    }
}


function parseHeader(tsv: File | undefined): void {
    if (!tsv) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        const content = e.target?.result;
        if (typeof content === 'string') {
            // extract first two rows
            const dataLines = content.split('\n').slice(0, 2)
            // Extract header
            header.value = [...dataLines[0].trim().split('\t')];
            const firstRowValues = dataLines[1].trim().split('\t')
            headerError.value = header.value.length < firstRowValues.length
            rows.value = [Object.fromEntries(firstRowValues.map((v, i) => {
                return [header.value[i], v]
            }))]
        } else {
            console.error('Failed to read file content.');
        }
    };

    reader.onerror = (e) => {
        console.error('Error occurred while reading the file.');
    };

    reader.readAsText(tsv);
}

const handleDragStart = (event: { dataTransfer: { setData: (arg0: string, arg1: string) => void } }, header: string) => {
    event.dataTransfer.setData('header', header);
};

const handleDrop = (event: { dataTransfer: { getData: (arg0: string) => any } }, key: string) => {
    const header = event.dataTransfer.getData('header')
    mappedFields.value[key] = header
};
</script>
<style scoped>
.drop-zone {
    background-color: #eee;
    margin-bottom: 10px;
    padding: 10px;
}

.drag-el {
    background-color: #fff;
    margin-bottom: 10px;
    padding: 1rem;
}
</style>