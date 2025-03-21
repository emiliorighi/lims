<template>
    <div v-if="metadata">
        <div v-for="field in fields" :key="field.key" class="row">
            <div v-if="isInputField(field.filter)" class="flex lg6 md6 sm12 xs12">
                <VaInput class="mb-2" @update:modelValue="(v: any) => emits('updateField', [field.key, v])"
                    :messages="[field.description]" :label="field.label" v-model="metadata[field.key]"
                    :rules="[requiredFieldRule(field.label, field.required)]" />
            </div>
            <div v-else-if="isSelectField(field.filter)" class="flex lg6 md6 sm12 xs12">
                <VaSelect class="mb-2" @update:modelValue="(v: any) => emits('updateField', [field.key, v])"
                    :messages="[field.description]" :label="field.label" v-model="metadata[field.key]"
                    :multiple="field.filter.multi" :options="field.filter.choices"
                    :rules="[requiredSelectRule(field.label, field.required)]" />
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { Filter, Input, Select, Range } from '../../data/types'

const props = defineProps<{
    fields: Filter[]
    existingMetadata?: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]][];
}>()

const metadata = ref<Record<string, any> | null>(null)

const requiredFieldRule = (label: string, required = true) => (v: any) => !required || (!!v) || `${label} is required`;
const requiredSelectRule = (label: string, required = true) => (v: any) => !required || (!!v) || `${label} is required`;

const emits = defineEmits(['updateField'])

onMounted(() => {
    metadata.value = null
    if (props.existingMetadata && props.existingMetadata.length) {
        metadata.value = { ...Object.fromEntries(props.existingMetadata) }
    } else {
        metadata.value = {}
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

</script>