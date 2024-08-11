<template>
    <VaSelect label="Input Type" v-model="input.input_type" :options="['text', 'number', 'date']" />
    <VaInput label="Regex" v-model="input.regex" />
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { Input } from './../../data/types';

const props = defineProps({
    value: Object as () => Input
});
const emit = defineEmits(['update:value']);

const input = ref({ ...props.value });

watch(input, (newValue) => {
    emit('update:value', newValue);
});
</script>