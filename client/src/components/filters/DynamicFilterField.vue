<template>
    <component :is="componentType" :field="field" :project-id="projectId" :model-name="modelName" :value="field.payload"
        @update="onUpdate" />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import TextFilterField from './TextFilterField.vue';
import SelectFilterField from './SelectFilterField.vue';
import NumberFilterField from './NumberFilterField.vue';
import DateFilterField from './DateFilterField.vue';

const props = defineProps<{
    field: { key: string; type: string; payload: Record<string, any> };
    projectId: string;
    modelName: string;
}>();

const emits = defineEmits<{
    (e: 'updateQuery', payload: { key: string; query: Record<string, any> }): void;
}>();

const componentType = computed(() => {
    switch (props.field.type) {
        case 'select':
            return SelectFilterField;
        case 'number':
            return NumberFilterField;
        case 'date':
            return DateFilterField;
        default:
            return TextFilterField;
    }
});

function onUpdate(query: Record<string, any>) {
    emits('updateQuery', { key: props.field.key, query });
}
</script>