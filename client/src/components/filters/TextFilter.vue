<template>
    <VaInput v-model="modelValue" clearable placeholder="Filter...">
        <template #prependInner>
            <VaIcon name="fa-search" color="secondary" />
        </template>
    </VaInput>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{ value: any }>();
const emit = defineEmits(['update:value']);

const modelValue = computed({
    get: () => props.value,
    set: (val) => emit('update:value', val),
});
</script>