<template>
    <div v-if="field.type === 'select'" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <RecordSelectFilter :field="field.key" :model-name="modelName" :project-id="projectId" :value="queryValue"
                v-if="field.type === 'select'" @value-change="(v: string) => queryValue = v" />
        </div>
    </div>
    <div class="row" v-else-if="field.type === 'text'">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput background="backgroundSecondary" :label="field.key" clearable v-model="queryValue"
                @update:model-value="(v: string) => queryValue = v">
            </VaInput>
        </div>
    </div>
    <div class="row" v-else>
        <div class="flex lg12 md12 sm12 xs12">
            <VaDropdown :close-on-content-click="false" stick-to-edges>
                <template #anchor>
                    <VaInput background="backgroundSecondary" :label="field.key" readonly :model-value="values">
                        <template #appendInner>
                            <VaIcon v-if="values" color="secondary" name="highlight_off" @click="query = {}"></VaIcon>
                        </template>
                    </VaInput>
                </template>
                <VaDropdownContent>
                    <div class="layout va-gutter-3 fluid">
                        <div class="row justify-end">
                            <div class="flex">
                                <VaRadio v-model="filterOpt" text-by="text" value-by="value" track-by="value"
                                    :options="options" />
                            </div>
                            <div v-if="field.type === 'date'" class="flex lg12 md12 sm12 xs12">
                                <VaDatePicker inner-label :label="field.key" style="width: 100%;" clearable
                                    v-if="filterOpt === 'single'" v-model="singleDateModel"
                                    @update:model-value="handleDate" />
                                <VaDatePicker clearable inner-label :label="field.key" style="width: 100%;" mode="range"
                                    v-model="rangeDateModel" @update:model-value="handleRangeDate" v-else />
                            </div>
                            <div v-else class="flex lg12 md12 sm12 xs12">
                                <VaInput :label="field.key" v-if="filterOpt === 'single'" v-model="queryValue"
                                    @update:model-value="(v: string) => queryValue = v" clearable />
                                <div v-else class="row justify-space-between align-center">
                                    <div class="flex lg6 md6 sm12 xs12">
                                        <VaInput :label="`from ${field.key}`" inner-label clearable v-model="rangeStart"
                                            @update:model-value="(v: string) => rangeStart = v">
                                        </VaInput>
                                    </div>
                                    <div class="flex lg6 md6 sm12 xs12">
                                        <VaInput :label="`to ${field.key}`" inner-label clearable v-model="rangeEnd"
                                            @update:model-value="(v: string) => rangeEnd = v">
                                        </VaInput>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </VaDropdownContent>
            </VaDropdown>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { InputType } from '../../data/types';
import RecordSelectFilter from './RecordSelectFilter.vue';

const props = defineProps<{
    field: { key: string; type: InputType; payload: Record<string, any> };
    projectId: string;
    modelName: string;
}>();

const emits = defineEmits(['updateQuery']);

const filterOpt = ref<'single' | 'range'>('single');

const values = computed(() => Object.values(props.field.payload).length > 1 ? Object.values(props.field.payload).join('-') : Object.values(props.field.payload)[0])


const singleDateModel = ref(null);
const rangeDateModel = ref<{ start: Date | null, end: Date | null }>({ start: null, end: null });

const options = [
    { text: 'Single', value: 'single' },
    { text: 'Range', value: 'range' }
];


onMounted(() => {
    if (rangeStart.value || rangeEnd.value) filterOpt.value = 'range'
    if (props.field.type === 'date') {
        const start = parseDate(rangeStart.value)
        const end = parseDate(rangeEnd.value)
        rangeDateModel.value = { start, end }
    }
})
// Computed access to payload
const query = computed({
    get() {
        return props.field.payload;
    },
    set(query: Record<string, any>) {
        emits('updateQuery', { key: props.field.key, query });
    }
});

// Dynamic query key (non-range)
const queryKey = computed(() => {
    if (props.field.type === 'select') {
        return `${props.field.key}__in`;
    }
    if (props.field.type === 'text') {
        return `${props.field.key}__icontains`;
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

watch(filterOpt, (newVal, oldVal) => {
    if (props.field.type === 'number' && oldVal === 'single' && newVal === 'range') {
        query.value = {};
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
        [gteKey.value]: payload && payload.start ? formatDate(payload.start) : null,
        [lteKey.value]: payload && payload.end ? formatDate(payload.end) : null
    };
}

function formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function parseDate(dateStr: string): Date | null {
    if (!dateStr) return null
    const [year, month, day] = dateStr.split('-').map(Number);
    return new Date(year, month - 1, day); // Month is 0-based in JS Date
}

</script>
