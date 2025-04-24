<template>
    <VaInput clearable :label="field.key" v-model="input" />
</template>

<script setup lang="ts">
import { ref, watch, toRefs, computed } from 'vue';

const props = defineProps<{
    field: { key: string };
    value: Record<string, any>;
}>();

const emits = defineEmits<{
    (e: 'update', value: Record<string, any>): void;
}>();

const { field, value } = toRefs(props);
const key = computed(() => `${field.value.key}__icontains`)
const input = ref(value.value[key.value] ?? '');

watch(input, (v) => {
    emits('update', { [key.value]: v });
});

watch(value.value, () => {
    console.log(value.value)
})
</script>