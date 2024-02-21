<template>
    <VaModal close-button class="modal-crud" :model-value="!!model" @ok="ok" @cancel="cancel">
        <template #header>
            <h2 class="va-h2"> {{ isUpdate ? 'Editing' : 'Creating ' }} Item </h2>
        </template>
        <VaForm v-if="model" ref="modelForm">
            <div v-if="!isUpdate" class="row">
                <div class="flex">
                    <VaInput readonly label="Sample identifier" v-model="newModelId" :error="idAlreadyExists"
                        :rules="[(v: string) => v.length > 0 || 'Fill the required fields to generate the identifier', !idAlreadyExists || ['An item with this identifier already exists']]">
                    </VaInput>
                </div>
            </div>
            <div v-for="field in schemaModel.fields" class="row">
                <div v-if="isInputField(field.filter)" class="flex">
                    <VaInput :key="field.key" :disabled="disabledRule(field)" :messages="[field.description]"
                        :label="field.label" v-model="modelMetadata.metadata[field.key]" :rules="[(v: string) => !field.required || v.length > 0 || 'Field is required',
                        ]">
                    </VaInput>
                    <!-- TODO: ADD REGEX CHECK -->
                </div>
                <div v-else-if="isSelectField(field.filter)" class="flex">
                    <VaSelect :key="field.key" :disabled="disabledRule(field)" :messages="[field.description]"
                        :label="field.label" v-model="modelMetadata.metadata[field.key]" :multiple="field.filter.multi"
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
                        :min="field.filter.min" v-model="modelMetadata.metadata[field.key]" class="mt-10"
                        track-label-visible>
                        <template #trackLabel="{ value }">
                            <VaChip color="warning" size="small">
                                {{ value }}
                            </VaChip>
                        </template>
                    </VaSlider>
                    <VaInput :key="field.key" :rules="[(v: number) => !field.required || !isNaN(v) || 'Field is required',
                    ]" :messages="[field.description]" readonly v-model="modelMetadata.metadata[field.key]">
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
import { Filter, Input, Select, Range, SampleModel, ExperimentModel, ProjectModel } from '../../data/types'
import { computed, onMounted, reactive, ref, watchEffect } from 'vue';
import { useForm } from 'vuestic-ui'
import { AxiosError } from 'axios';

const props = defineProps<{
    schemaModel: ProjectModel,
    model: null | SampleModel | ExperimentModel,
    isUpdate: boolean,
    validIdCallback: Function
}>()

const modelMetadata = reactive<{
    metadata: Record<string, any>
}>(
    { metadata: {} }
)

const emits = defineEmits(['onOk', 'onCancel'])
const { schema } = useSchemaStore()
const { validate } = useForm('modelForm')
const idAlreadyExists = ref(false)

onMounted(() => {
    if (props.model) modelMetadata.metadata = { ...props.model.metadata }
})

const newModelId = computed(() => {
    if (props.model) return Object.entries(modelMetadata.metadata)
        .filter(([k, v]) => props.schemaModel.id_format.includes(k))
        .map(([k, v]) => v).join('_')
    return ''
})
const disabledRule = (filter: Filter) => props.schemaModel.id_format.includes(filter.key) && props.isUpdate

watchEffect(async () => {
    if (!newModelId.value || props.isUpdate) return
    try {
        const { data } = await props.validIdCallback(schema.project_id, newModelId.value)
        idAlreadyExists.value = true
    } catch (error) {
        const axiosError = error as AxiosError
        if (axiosError.response && axiosError.response.status === 404) {
            idAlreadyExists.value = false
            
        }
    }
})
const isInputField = (filter: Filter['filter']): filter is Input => {
    return (filter as Input).input_type !== undefined;
};

const isSelectField = (filter: Filter['filter']): filter is Select => {
    return (filter as Select).choices !== undefined;
};

const isRangeField = (filter: Filter['filter']): filter is Range => {
    return (filter as Range).min !== undefined;
};

function ok() {
    if (validate()) {
        emits('onOk', modelMetadata.metadata)
    }
}
function cancel() {
    emits('onCancel')
}
// //Should cheange between update and create
// async function submitSample() {
//     const { sample } = sampleStore
//     if (validate() && sample) {
//         try {
//             if (sampleStore.isUpdate) {
//                 const {data} = await SampleService.updateSample(schema.project_id, sample.sample_id, sample.metadata)
//                 toast({ color: 'success', message: data.join(', '), duration: 1500 })

//             } else {
//                 const { data } = await SampleService.createSample(schema.project_id, sample.metadata)
//                 toast({ color: 'success', message: data.join(', '), duration: 1500 })
//             }
//             emits('onSampleEdited')
//         } catch (error) {
//             toast({ color: 'danger', message: 'Impossible to save', duration: 1500 })
//         } finally {
//             resetSample()
//         }
//     }
// }
</script>
<style lang="scss" scoped>
.modal-crud {
    .VaInput {
        display: block;
    }
}
</style>