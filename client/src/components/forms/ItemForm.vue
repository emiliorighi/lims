<template>
    <div>
        <div v-for="field in fields" class="row">
            <div v-if="isInputField(field.filter)" class="flex lg6 md6">
                <VaInput @update:modelValue="(v: any) => updateMetadata([field.key, v])" class="mt-4"
                    :disabled="disabledRule(field)" :messages="[field.description]" :label="field.label"
                    v-model="metadata[field.key]" :rules="[(v: string) => !field.required || v.length > 0 || 'Field is required',
                ]" />
                <!-- ADD REGEX CHECK -->
            </div>
            <div v-else-if="isSelectField(field.filter)" class="flex lg6 md6">
                <VaSelect @update:modelValue="(v: any) => updateMetadata([field.key, v])" class="mt-4"
                    :disabled="disabledRule(field)" :messages="[field.description]" :label="field.label"
                    v-model="metadata[field.key]" :multiple="field.filter.multi" :options="field.filter.choices" :rules="[
                    (v: string | string[]) =>
                        !field.required ||
                        (Array.isArray(v) && v.length > 0)
                        || (v.length > 0)
                        || 'Field is required']" />
            </div>
            <div v-else-if="isRangeField(field.filter)" class="flex">
                <VaSlider 
                    @update:modelValue="(v: any) => updateMetadata([field.key, v])" 
                    class="mt-4"
                    :disabled="disabledRule(field)" 
                    :label="field.label" 
                    :max="field.filter.max" 
                    :min="field.filter.min"
                    v-model="metadata[field.key]" 
                    track-label-visible>
                        <template #trackLabel="{ value }">
                        <VaChip 
                            color="warning" 
                            size="small">
                            {{ value }}
                        </VaChip>
                    </template>
                </VaSlider>
                <VaInput class="mt-4" :rules="[(v: number) => !field.required || !isNaN(v) || 'Field is required',
                ]" :messages="[field.description]" readonly v-model="metadata[field.key]">
                    <template #appendInner>
                        <span>{{ field.filter.unit }}</span>
                    </template>
                </VaInput>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { Filter, Input, Select, Range } from '../../data/types';
import { onMounted, ref } from 'vue';


const props = defineProps<{
    fields: Filter[]
    id_format: string[],
    existingMetadata: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]][];
}>()

const emits = defineEmits(['updateField', 'updateId'])

const disabledRule = (filter: Filter) => props.id_format.includes(filter.key) && props.existingMetadata.length

const metadata = ref(Object.fromEntries(props.fields.map(f => [f.key, ''])))

onMounted(() => {
    if (props.existingMetadata.length) {
        metadata.value = { ...Object.fromEntries(props.existingMetadata) }
    } else {
        metadata.value = { ...Object.fromEntries(props.fields.map(f => [f.key, ''])) }
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

function updateMetadata(tuple: [keyof Record<string, any>, Record<string, any>[keyof Record<string, any>]]) {
    emits('updateField', tuple)
}


</script>