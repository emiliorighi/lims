<template>
    <div class="row align-center justify-space-between">
        <div style="padding-top: 0;padding-bottom: 0;" class="flex">
            <span class="va-text-bold">{{ field.key }}</span>
        </div>
        <div style="padding-top: 0;padding-bottom: 0;" v-if="rangeEnabled" class="flex">
            <VaRadio v-model="filterOpt" text-by="text" value-by="value" track-by="value"
                @update:model-value="handleMode" :options="options" />
        </div>
    </div>
    <div v-if="field.type === 'select'" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <RecordSelectFilter :field="field.key" :model-name="modelName" :project-id="projectId"
                :value="query[`${field.key}__in`]" v-if="field.type === 'select'"
                @value-change="(v: string) => handleValue(`${field.key}__in`, v)" />
        </div>
    </div>
    <div class="row" v-else-if="field.type === 'text'">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput clearable v-model="query[`${field.key}__in`]"
                @update:model-value="(v: string) => handleValue(`${field.key}__in`, v)">
            </VaInput>
        </div>
    </div>
    <div class="row" v-else-if="field.type === 'number'">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput v-if="filterOpt === 'single'" v-model="query[field.key]"
                @update:model-value="(v: string) => handleValue(field.key, v)" />
            <div v-else>
                <div v-if="field.type === 'number'" class="row justify-space-between align-center">
                    <div class="flex lg6 md6">
                        <VaInput clearable v-model="query[`${field.key}__gte`]"
                            @update:model-value="(v: string) => handleValue(`${field.key}__gte`, v)">
                            <template #prepend>
                                <VaButton preset="secondary" color="textPrimary">
                                    From
                                </VaButton>
                            </template>
                        </VaInput>
                    </div>
                    <div class="flex lg6 md6">
                        <VaInput clearable v-model="query[`${field.key}__lte`]"
                            @update:model-value="(v: string) => handleValue(`${field.key}__lte`, v)">
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
import { computed, ref, watch } from 'vue';
import { ResearchFilter } from '../../data/types';
import RecordSelectFilter from './RecordSelectFilter.vue';
import { useRecordStore } from '../../stores/record-store';

const props = defineProps<{
    field: ResearchFilter
    projectId: string,
    modelName: string,
    query: Record<string, any>
}>()

const emits = defineEmits(['updateQuery'])

const options = [
    {
        text: 'Single Value',
        value: 'single'
    },
    {
        text: 'Range',
        value: 'range'
    },
]

const filterOpt = ref<'single' | 'range'>('single')
const singleDateModel = ref(null)
const rangeDateModel = ref({ start: null, end: null })

// watch(() => filterOpt.value, () => {
//     emits('updateQuery', {
//         key: props.field.key, query: initQuery(undefined, filterOpt.value)
//     })
// })



const query = computed({
    get() {
        console.log('getter')
        return initQuery(props.query)
    },
    set(query: Record<string, any>) {
        emits('updateQuery', { key: props.field.key, query })
    }
})

const rangeEnabled = computed(() => props.field.type === 'date' || props.field.type === 'number')

function initQuery(query: Record<string, any> | undefined) {
    console.log('QUery is')
    console.log(query)
    if (query) {
        //check if keys contains range
        const hasRange = Object.keys(query).filter(k => k.includes('__lte') || k.includes('__gte')).length > 0
        filterOpt.value = hasRange ? 'range' : 'single'
        return query
    }
    else {
        // if (range === 'range') return Object.fromEntries([[`${props.field.key}__lte`, null], [`${props.field.key}__gte`, null]])
        if (props.field.type === 'date' || props.field.type === 'number') return Object.fromEntries([[props.field.key, null]])
        return Object.fromEntries([[`${props.field.key}__in`, null]])
    }
}

function handleMode(v: 'single' | 'range') {
    console.log('HERe')
    console.log(v)
}
function handleValue(key: string, v: string | undefined) {
    query.value = { ...query.value, ...Object.fromEntries([[key, v]]) }
}

function handleDate(date: Date) {
    query.value = { [props.field.key]: date ? formatDate(date) : null }
}

function handleRangeDate(payload: { start: Date, end: Date }) {
    console.log(payload)
    query.value = {
        [`${props.field.key}__gte`]: payload.start ? formatDate(payload.start) : null,
        [`${props.field.key}__lte`]: payload.end ? formatDate(payload.end) : null
    }
    console.log(query.value)
}

function formatDate(date: Date) {
    return date.toISOString().substring(0, 10)
}
</script>