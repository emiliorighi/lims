<template>
    <VaForm ref="itemForm">
        <div class="row">
            <VaInput class="flex" readonly label="Unique identifier" v-model="itemId"
                :rules="[(v: string) => v.length > 0 || 'Fill the required fields to generate the unique identifier']">
            </VaInput>
        </div>
        <div v-for="field in fields" class="row">
            <div v-if="isInputField(field.filter)" class="flex">
                <VaInput :disabled="disabledRule(field)" :messages="[field.description]" :label="field.label"
                    v-model="metadata[field.key]" :rules="[(v: string) => !field.required || v.length > 0 || 'Field is required',
            ]" />
                <!-- ADD REGEX CHECK -->
            </div>
            <div v-else-if="isSelectField(field.filter)" class="flex">
                <VaSelect :disabled="disabledRule(field)" :messages="[field.description]" :label="field.label"
                    v-model="metadata[field.key]" :multiple="field.filter.multi" :options="field.filter.choices" :rules="[
                (v: string | string[]) =>
                    !field.required ||
                    (Array.isArray(v) && v.length > 0)
                    || (v.length > 0)
                    || 'Field is required']" />
            </div>
            <div v-else-if="isRangeField(field.filter)" class="flex">
                <VaSlider :disabled="disabledRule(field)" :label="field.label" :max="field.filter.max"
                    :min="field.filter.min" v-model="metadata[field.key]" class="mt-10" track-label-visible>
                    <template #trackLabel="{ value }">
                        <VaChip color="warning" size="small">
                            {{ value }}
                        </VaChip>
                    </template>
                </VaSlider>
                <VaInput :rules="[(v: number) => !field.required || !isNaN(v) || 'Field is required',
            ]" :messages="[field.description]" readonly v-model="metadata[field.key]">
                    <template #appendInner>
                        <span>{{ field.filter.unit }}</span>
                    </template>
                </VaInput>
            </div>
        </div>
        <VaDivider />
        <div class="row justify-space-between">
            <div class="flex">
                <VaButton @click="validateMetadata">Submit</VaButton>
            </div>
            <div class="flex">
                <VaButton color="danger" @click="reset">Cancel</VaButton>
            </div>
        </div>
    </VaForm>
</template>
<script setup lang="ts">
import { useForm } from 'vuestic-ui/web-components';
import { Filter, Input, Select, Range } from '../../data/types';
import { computed, onMounted, ref } from 'vue';


const props = defineProps<{
    fields: Filter[]
    id_format: string[],
    existingMetadata: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]][];
}>()

const { validate } = useForm('itemForm')

const emits = defineEmits(['onMetadataValid', 'onReset'])

const disabledRule = (filter: Filter) => props.id_format.includes(filter.key) && props.existingMetadata.length

const metadata = ref(Object.fromEntries(props.fields.map(f => [f.key, ''])))


onMounted(() => {
    if (props.existingMetadata.length) {
        metadata.value = { ...Object.fromEntries(props.existingMetadata) }
    } else {
        metadata.value = { ...Object.fromEntries(props.fields.map(f => [f.key, ''])) }
    }
})
const itemId = computed(() => {
    return Object.entries(metadata.value)
        .filter(([k, v]) => v && props.id_format.includes(k))
        .map(([k, v]) => v).join('_')
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

function reset() {
    metadata.value = { ...Object.fromEntries(props.fields.map(f => [f.key, ''])) }
    emits('onReset')
}

function validateMetadata() {
    if (validate()) emits('onMetadataValid', metadata.value)
}

</script>