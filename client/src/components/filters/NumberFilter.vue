<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput type="number" v-model="modelValue" :placeholder="queryOperator === 'range' ? 'From' : 'Filter...'">
                <template #prependInner>
                    <VaIcon name="fa-search" color="secondary" />
                </template>
            </VaInput>
        </div>
        <div v-if="queryOperator === 'range'" class="flex lg12 md12 sm12 xs12">
            <VaInput type="number" v-model="modelSecondValue" placeholder="To">
                <template #prependInner>
                    <VaIcon name="fa-search" color="secondary" />
                </template>
            </VaInput>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { QueryOperator } from '../../data/types';

const props = defineProps<{ value: any; secondValue: any; queryOperator: QueryOperator }>();
const emit = defineEmits(['update:value', 'update:secondValue']);

const modelValue = computed({
    get: () => props.value,
    set: (val) => emit('update:value', val),
});

const modelSecondValue = computed({
    get: () => props.secondValue,
    set: (val) => emit('update:secondValue', val),
});
</script>