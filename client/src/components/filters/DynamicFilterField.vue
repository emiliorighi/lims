<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaSelect :options="options" v-model="queryOperator" @update:model-value="handleOpUpdate" trackBy="label"
                valueBy="key" textBy="label">
            </VaSelect>
        </div>
        <!-- Query Input Field -->
        <div class="flex lg12 md12 sm12 xs12">
            <component :is="componentType" :value="value" :second-value="secondValue" :choices="field.choices"
                :query-operator="queryOperator" @update:value="updateValue" @update:secondValue="updateSecondValue" />
        </div>

        <div class="flex lg12 md12 sm12 xs12">
            <VaButton color="textPrimary" preset="primary" @click="resetFields" block>Reset</VaButton>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import TextFilter from './TextFilter.vue';
import SelectFilter from './ListFilter.vue';
import NumberFilter from './NumberFilter.vue';
import DateFilter from './DateFilter.vue';
import { stringQueryOperators, numberDateQueryOperators, listQueryOperators, QueryOperator } from '../../data/types'

const props = defineProps<{
    field: { key: string; type: string; payload: Record<QueryOperator, any>, choices?: string[] };
    projectId: string;
    modelName: string;
}>();

const emits = defineEmits<{
    (e: 'updateQuery', payload: { key: string; query: Record<string, any> }): void;
}>();

const queryOperator = ref<QueryOperator | null>(null)
const value = ref<any>(null)
const secondValue = ref<any>(null)


const componentType = computed(() => {
    switch (props.field.type) {
        case 'select':
            return SelectFilter;
        case 'number':
            return NumberFilter;
        case 'date':
            return DateFilter;
        default:
            return TextFilter;
    }
});

watch(() => props.field.payload, (payload) => {
    //range of values
    if ('gte' in payload && 'lte' in payload) {
        queryOperator.value = 'range'
        value.value = payload.gte
        secondValue.value = payload.lte
    }
    else {
        const [key, v] = Object.entries(payload)[0]
        queryOperator.value = key as QueryOperator
        value.value = v
    }

}, { deep: true, immediate: true })

function updateValue(newValue: any) {
    value.value = newValue;
}

function updateSecondValue(newValue: any) {
    secondValue.value = newValue;
}

watch([value, secondValue], ([v1, v2]) => {
    if (queryOperator.value === 'range') {
        emits('updateQuery', { key: props.field.key, query: { gte: v1, lte: v2 } });
    } else {
        emits('updateQuery', { key: props.field.key, query: { [queryOperator.value!]: v1 } });
    }
});
function handleOpUpdate(op: QueryOperator) {
    if (op !== 'range') {
        if (value.value !== null) {
            const entry = [[queryOperator.value, value.value]]
            emits('updateQuery', { key: props.field.key, query: Object.fromEntries(entry) });
        }
    }
}

function resetFields() {
    value.value = null;
    secondValue.value = null;
}
const queryType = computed(() => {
    switch (props.field.type) {
        case 'select':
            return listQueryOperators;
        case 'text':
            return stringQueryOperators;
        default:
            return numberDateQueryOperators;
    }
})

const options = computed(() => Object.entries(queryType.value).map(([k, v]) => ({ key: k, label: v })))


</script>