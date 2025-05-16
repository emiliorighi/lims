<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaDateInput :format-date="formatDate" :placeholder="queryOperator === 'range' ? 'From' : 'Filter...'"
                style="width: 100%;" v-model="modelValue" />
        </div>
        <div v-if="queryOperator === 'range'" class="flex lg12 md12 sm12 xs12">
            <VaDateInput :format-date="formatDate" placeholder="To" style="width: 100%;" v-model="modelSecondValue" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { QueryOperator } from '../../data/types';
import { formatDate } from '../../composables/formatDate';

const props = defineProps<{ value: any; secondValue: any; queryOperator: QueryOperator }>();
const emit = defineEmits(['update:value', 'update:secondValue']);

const modelValue = computed({
    get: () => props.value,
    set: (val) => emit('update:value', val instanceof Date ? formatDate(val) : val),
});

const modelSecondValue = computed({
    get: () => props.secondValue,
    set: (val) => emit('update:secondValue', val instanceof Date ? formatDate(val) : val),
});


</script>