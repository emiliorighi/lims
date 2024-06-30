<template>
    <div class="row">
        <div class="flex">
            <VaInput iconColor="primary" v-model="searchForm.filter" clearable
                @update:modelValue="(v: string) => emits('onSearchChange', ['filter', v])"
                placeholder="Type to search..">
                <template #appendInner>
                    <va-icon name="search" />
                </template>
            </VaInput>
        </div>
        <div v-if="showFields.length" class="flex">
            <VaButtonDropdown :closeOnContentClick="false" icon="hide_source" preset="primary" label="Fields"
                class="mr-2 mb-2">
                <div class="row row-drop-down">
                    <div class="flex lg7 md7 sm12 xs12" v-for="(field, index) in showFields">
                        <VaSwitch class="mt-2" :key="index" v-model="showFields[index].show" :label="field.value"
                            size="small" />
                    </div>
                </div>
            </VaButtonDropdown>
        </div>
        <div v-if="searchForm.query" class="flex">
            <VaBadge style="z-index: 1;" overlap color="info" :text="activeFilters">
                <VaButtonDropdown :closeOnContentClick="false" icon="filter_list" label="Filters" preset="primary"
                    class="mr-2 mb-2">
                    <div class="row row-drop-down">
                        <div class="flex lg12 md12 sm12 xs12" v-for="(field, index) in fields" :key="index">
                            <VaInput @update:modelValue="(v: string) => onQueryUpdate(v, field)" class="mt-2" clearable
                                :label="field.key" v-if="isInputField(field.filter)"
                                v-model="searchForm.query[field.key]">
                            </VaInput>
                            <VaSelect class="mt-2" @update:modelValue="(v: any) => onQueryUpdate(v, field)" clearable
                                :label="field.key" v-else-if="isSelectField(field.filter)"
                                v-model="searchForm.query[field.key]" :multiple="field.filter.multi"
                                :options="field.filter.choices">
                            </VaSelect>
                            <VaSlider :label="field.label" v-else-if="isRangeField(field.filter)"
                                @update:modelValue="(v: any) => onQueryUpdate(v, field)"
                                v-model="searchForm.query[field.key]" class="mt-4" :min="field.filter.min"
                                :max="field.filter.max" range track-label-visible>
                                <template #trackLabel="{ value, order }">
                                    <VaChip size="small" :color="order === 0 ? 'secondary' : 'warning'">
                                        {{ value }}
                                    </VaChip>
                                </template>
                            </VaSlider>
                        </div>
                    </div>
                </VaButtonDropdown>
            </VaBadge>
        </div>
        <div class="flex">
            <VaBadge style="z-index: 1;" overlap color="warning" :text="searchForm.sort_column">
                <VaButtonDropdown preset="primary" :closeOnContentClick="false" label="Sort" icon="sort"
                    class="mr-2 mb-2">
                    <div class="row row-drop-down">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaSelect clearable class="mt-2" label="Sort Field"
                                @update:modelValue="(v: string) => emits('onSearchChange', ['sort_column', v])"
                                v-model="searchForm.sort_column" :options="fields.map(f => f.key)" />
                        </div>
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaSelect clearable class="mt-2" label="Sort Order"
                                @update:modelValue="(v: string) => emits('onSearchChange', ['sort_order', v])"
                                v-model="searchForm.sort_order" :options="['asc', 'desc']" />
                        </div>
                    </div>
                </VaButtonDropdown>
            </VaBadge>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watchEffect } from 'vue';
import { Filter, Input, Select, Range, ModelSearchForm } from '../../data/types'

const props = defineProps<{
    columns: string[],
    fields: Filter[],
}>()


onMounted(() => {
    searchForm.value.query = { ...createFilters(props.fields) }
})

const activeFilters = computed(() => {

    const entries = Object.entries(searchForm.value.query)

    const inputs = entries.filter(([k, v]) => !!v && !Array.isArray(v))

    //check ranges
    const ranges = entries.filter(([k, v]) => Array.isArray(v))
    const filteredRanges: any[][] = []
    ranges.forEach(([k, v]) => {
        const [minV, maxV] = v
        //get filter
        const filter = props.fields.find(f => f.key === k)
        if (filter && isRangeField(filter.filter)) {
            const { min, max } = filter.filter
            if (minV !== min || maxV !== max) {
                filteredRanges.push([k, v])
            }
        }
    })
    return [...inputs, ...filteredRanges].length
})
const searchForm = ref<ModelSearchForm>({
    query: {},
    filter: '',
    sort_column: '',
    sort_order: 'asc'
})

const emits = defineEmits(['onMetadataUpdate', 'onShowFieldChange', 'onSearchChange'])

const showFields = ref(props.fields.map((filter: Filter) => {
    return {
        show: filter.required,
        value: filter.key
    }
}))

watchEffect(() => {
    emits('onShowFieldChange', showFields.value)
})

function onQueryUpdate(v: any, field: Filter) {
    const { filter } = field
    const list = []
    if (isInputField(filter)) {
        const tuple = [field.key, v]
        list.push(tuple)
    } else if (isSelectField(filter)) {
        const tuple = [field.key, filter.multi ? v.join(', ') : v]
        list.push(tuple)
    } else {
        const [min, max] = v
        const lteTuple = [`${field.key}__lte`, max]
        const gteTuple = [`${field.key}__gte`, min]
        list.push(lteTuple)
        list.push(gteTuple)

    }
    emits('onMetadataUpdate', list)

}

function createFilters(fields: Filter[]) {
    const entries = fields.map(f => {
        if (isInputField(f.filter)) {
            return [f.key, '']
        } else if (isSelectField(f.filter)) {
            return f.filter.multi ? [f.key, ['']] : [f.key, '']
        } else {
            return [f.key, [f.filter.min, f.filter.max]]
        }
    })
    return Object.fromEntries(entries)
}

const isInputField = (filter: Filter['filter']): filter is Input => {
    return (filter as Input).input_type !== undefined;
};

const isSelectField = (filter: Filter['filter']): filter is Select => {
    return (filter as Select).choices !== undefined;
};

const isRangeField = (filter: Filter['filter']): filter is Range => {
    return (filter as Range).min !== undefined;
};

</script>
<style scoped>
.row-drop-down {
    width: min-content;
    max-height: 400px;
    overflow: scroll;
    padding: 16px;
}
</style>
