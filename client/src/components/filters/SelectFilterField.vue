<template>
    <RecordSelectFilter :field="field" :model-name="modelName" :project-id="projectId" :value="selected"
        @value-change="handleChange" />
</template>

<script setup lang="ts">
import { ref, watch, toRefs } from 'vue';
import RecordSelectFilter from './RecordSelectFilter.vue';

const props = defineProps<{
    field: { key: string };
    modelName: string;
    projectId: string;
    value: Record<string, any>;
}>();

const emits = defineEmits<{
    (e: 'update', value: Record<string, any>): void;
}>();

const { field, value } = toRefs(props);

// Construct query key for select field (usually "__in")
const key = `${field.value.key}__in`;

// Local selected value (assuming single string or array of strings)
const selected = ref(value.value[key] ?? '');

// Sync if parent prop changes externally
watch(value, (newVal) => {
    selected.value = newVal[key] ?? '';
});

// Emit updated value when changed
function handleChange(v: string | string[]) {
    selected.value = v;
    emits('update', { [key]: v });
}
</script>