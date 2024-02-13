<template>
    <VaModal close-button class="modal-crud" :model-value="!!sampleStore.sample" @ok="submitSample" @cancel="resetSample()">
        <template #header>
            <h2 class="va-h2"> Editing sample </h2>
        </template>
        <VaForm v-if="sampleStore.sample" ref="sampleForm">
            <div v-if="sampleStore.isUpdate" class="row">
                <div class="flex">
                    <h2 class="va-h2">{{ sampleStore.sample.sample_id }}</h2>
                </div>
            </div>
            <div v-else class="row">
                <div class="flex">
                    <VaInput readonly label="Sample identifier" v-model="newSampleId" :error="idAlreadyExists"
                        :rules="[(v: string) => v.length > 0 || 'Fill the required fields to generate the sample identifier', !idAlreadyExists || ['A sample with this identifier already exists']]">
                    </VaInput>
                </div>
            </div>
            <div v-for="field in schema.sample.fields" class="row">
                <div v-if="isInputField(field.filter)" class="flex">
                    <VaInput :key="field.key" :disabled="disabledRule(field)" :messages="[field.description]"
                        :label="field.label" v-model="sampleStore.sample.metadata[field.key]" :rules="[(v: string) => !field.required || v.length > 0 || 'Field is required',
                        ]">
                    </VaInput>
                    <!-- ADD REGEX CHECK -->
                </div>
                <div v-else-if="isSelectField(field.filter)" class="flex">
                    <VaSelect :key="field.key" :disabled="disabledRule(field)" :messages="[field.description]"
                        :label="field.label" v-model="sampleStore.sample.metadata[field.key]" :multiple="field.filter.multi"
                        :options="field.filter.choices" :rules="[
                            (v: string | string[]) =>
                                !field.required ||
                                (Array.isArray(v) && v.length > 0)
                                || (v.length > 0)
                                || 'Field is required']">
                    </VaSelect>
                </div>
                <div v-else-if="isRangeField(field.filter)" class="flex">
                    <VaSlider :key="field.key" :disabled="disabledRule(field)" :label="field.label" :max="field.filter.max"
                        :min="field.filter.min" v-model="sampleStore.sample.metadata[field.key]" class="mt-10"
                        track-label-visible>
                        <template #trackLabel="{ value }">
                            <VaChip color="warning" size="small">
                                {{ value }}
                            </VaChip>
                        </template>
                    </VaSlider>
                    <VaInput :key="field.key" :rules="[(v: number) => !field.required || !isNaN(v) || 'Field is required',
                    ]" :messages="[field.description]" readonly v-model="sampleStore.sample.metadata[field.key]">
                        <template #appendInner>
                            <span>{{ field.filter.unit }}</span>
                        </template>
                    </VaInput>
                </div>
            </div>
        </VaForm>
    </VaModal>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useSampleStore } from '../../stores/sample-store';
import { Filter, Input, Select, Range } from '../../data/types'
import { computed, ref, watchEffect } from 'vue';
import SampleService from '../../services/clients/SampleService'
import { useGlobalStore } from '../../stores/global-store';
import { useForm } from 'vuestic-ui'
import { AxiosError } from 'axios';

const emits = defineEmits(['onSampleEdited'])
const { schema } = useSchemaStore()
const sampleStore = useSampleStore()
const { validate } = useForm('sampleForm')
const idAlreadyExists = ref(false)
const newSampleId = computed(() => {
    if (sampleStore.sample) return Object.entries(sampleStore.sample.metadata)
        .filter(([k, v]) => schema.sample.id_format.includes(k))
        .map(([k, v]) => v).join('_')
    return ''
})
const { toast } = useGlobalStore()

const disabledRule = (filter: Filter) => schema.sample.id_format.includes(filter.key) && sampleStore.isUpdate

watchEffect(async () => {
    if (!newSampleId.value || sampleStore.isUpdate) return
    try {
        const { data } = await SampleService.getSample(schema.project_id, newSampleId.value)
        idAlreadyExists.value = true
    } catch (error) {
        const axiosError = error as AxiosError
        if (axiosError.response && axiosError.response.status === 404) {
            idAlreadyExists.value = false
        }
    } finally {
        if (sampleStore.sample) sampleStore.sample.sample_id = newSampleId.value
    }
})

function resetSample() {
    sampleStore.sample = null
}

const isInputField = (filter: Filter['filter']): filter is Input => {
    return (filter as Input).input_type !== undefined;
};

const isSelectField = (filter: Filter['filter']): filter is Select => {
    return (filter as Select).choices !== undefined;
};

const isRangeField = (filter: Filter['filter']): filter is Range => {
    return (filter as Range).min !== undefined;
};

//Should cheange between update and create
async function submitSample() {
    const { sample } = sampleStore
    if (validate() && sample) {
        try {
            if (sampleStore.isUpdate) {
                const {data} = await SampleService.updateSample(schema.project_id, sample.sample_id, sample.metadata)
                toast({ color: 'success', message: data.join(', '), duration: 1500 })

            } else {
                const { data } = await SampleService.createSample(schema.project_id, sample.metadata)
                toast({ color: 'success', message: data.join(', '), duration: 1500 })
            }
            emits('onSampleEdited')
        } catch (error) {
            toast({ color: 'danger', message: 'Impossible to save', duration: 1500 })
        } finally {
            resetSample()
        }
    }
}
</script>
<style lang="scss" scoped>
.modal-crud {
    .VaInput {
        display: block;
    }
}
</style>