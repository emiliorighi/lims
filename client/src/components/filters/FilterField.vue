<template>
    <div class="row align-center justify-space-between">
        <div style="padding-top: 0;padding-bottom: 0;" class="flex">
            <span class="va-text-bold">{{ field.key }}</span>
        </div>
        <div style="padding-top: 0;padding-bottom: 0;" v-if="rangeEnabled" class="flex">
            <VaRadio v-model="filterOpt" text-by="text" value-by="value" track-by="value" :options="options" />
        </div>
    </div>
    <div v-if="field.type === 'select'" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <RecordSelectFilter :field="field.key" :model-name="modelName" :project-id="projectId" :value="queryValue"
                v-if="field.type === 'select'" @value-change="(v: string) => queryValue = v" />
        </div>
    </div>
    <div class="row" v-else-if="field.type === 'text'">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput clearable v-model="queryValue" @update:model-value="(v: string) => queryValue = v">
            </VaInput>
        </div>
    </div>
    <div class="row" v-else-if="field.type === 'number'">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput v-if="filterOpt === 'single'" v-model="queryValue"
                @update:model-value="(v: string) => queryValue = v" />
            <div v-else>
                <div v-if="field.type === 'number'" class="row justify-space-between align-center">
                    <div class="flex lg6 md6">
                        <VaInput clearable v-model="rangeStart" @update:model-value="(v: string) => rangeStart = v">
                            <template #prepend>
                                <VaButton preset="secondary" color="textPrimary">
                                    From
                                </VaButton>
                            </template>
                        </VaInput>
                    </div>
                    <div class="flex lg6 md6">
                        <VaInput clearable v-model="rangeEnd" @update:model-value="(v: string) => rangeEnd = v">
                            <template #prepend>
                                <VaButton preset="secondary" color="textPrimary">
                                    To
                                </VaButton>
                            </template>
                        </VaInput>
                    </div>
                </div>
            </div>

        </div>
    </div>
    <div class="row" v-else>
        <div class="flex lg12 md12 sm12 xs12">
            <VaDateInput style="width: 100%;" clearable v-if="filterOpt === 'single'" v-model="singleDateModel"
                @update:model-value="handleDate" />
            <VaDateInput style="width: 100%;" mode="range" v-model="rangeDateModel"
                @update:model-value="handleRangeDate" v-else />
        </div>
    </div>

</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { InputType } from '../../data/types';
import RecordSelectFilter from './RecordSelectFilter.vue';

const props = defineProps<{
    field: { key: string; type: InputType; payload: Record<string, any> };
    projectId: string;
    modelName: string;
}>();

const emits = defineEmits(['updateQuery']);

const filterOpt = ref<'single' | 'range'>('single');

const singleDateModel = ref(null);
const rangeDateModel = ref({ start: null, end: null });

const options = [
    { text: 'Single Value', value: 'single' },
    { text: 'Range', value: 'range' }
];


// Computed access to payload
const query = computed({
    get() {
        return props.field.payload;
    },
    set(query: Record<string, any>) {
        emits('updateQuery', { key: props.field.key, query });
    }
});

const rangeEnabled = computed(() => ['date', 'number'].includes(props.field.type));

// Dynamic query key (non-range)
const queryKey = computed(() => {
    if (props.field.type === 'select' || props.field.type === 'text') {
        return `${props.field.key}__in`;
    }
    if (props.field.type === 'number' && filterOpt.value === 'single') {
        return props.field.key;
    }
    if (props.field.type === 'date' && filterOpt.value === 'single') {
        return props.field.key;
    }
    return null;
});

const queryValue = computed({
    get() {
        return queryKey.value ? query.value[queryKey.value] : null;
    },
    set(v) {
        if (queryKey.value) {
            query.value = { ...query.value, [queryKey.value]: v };
        }
    }
});

// Range keys for number/date
const gteKey = computed(() => `${props.field.key}__gte`);
const lteKey = computed(() => `${props.field.key}__lte`);

const rangeStart = computed({
    get: () => query.value[gteKey.value],
    set: (v) => {
        query.value = { ...query.value, [gteKey.value]: v };
    }
});

const rangeEnd = computed({
    get: () => query.value[lteKey.value],
    set: (v) => {
        query.value = { ...query.value, [lteKey.value]: v };
    }
});

function handleDate(date: Date | null) {
    query.value = {
        [props.field.key]: date ? formatDate(date) : null
    };
}

function handleRangeDate(payload: { start: Date | null; end: Date | null }) {
    query.value = {
        [gteKey.value]: payload.start ? formatDate(payload.start) : null,
        [lteKey.value]: payload.end ? formatDate(payload.end) : null
    };
}

function formatDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
</script>
