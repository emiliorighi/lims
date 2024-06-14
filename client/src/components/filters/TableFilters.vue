<template>
    <div class="row">
        <div v-if="showFields.length" class="flex">
            <VaButtonDropdown :closeOnContentClick="false" icon="hide_source" preset="primary" label="Fields"
                class="mr-2 mb-2">
                <div class="w-200 row justify-center">
                    <div class="flex lg12 md12 sm12 xs12" v-for="(field, index) in showFields">
                        <VaSwitch class="mt-2" :key="index" v-model="showFields[index].show" :label="field.value"
                            size="small" />
                    </div>
                </div>
            </VaButtonDropdown>
        </div>
        <div class="flex">
            <VaButtonDropdown :closeOnContentClick="false" icon="filter_list" label="Filters" preset="primary"
                class="mr-2 mb-2">
                <div class="w-200">
                    <div v-for="(field, index) in fields" :key="index">
                        <VaInput class="mt-2" clearable :label="field.key" v-if="isInputField(field.filter)"
                            v-model="searchForm.filters[field.key]">
                        </VaInput>
                        <VaSelect class="mt-2" clearable :label="field.key" v-else-if="isSelectField(field.filter)"
                            v-model="searchForm.filters[field.key]" :multiple="field.filter.multi"
                            :options="field.filter.choices">
                        </VaSelect>
                        <VaSlider class="mt-2" range :label="field.key" v-else-if="isRangeField(field.filter)"
                            v-model="searchForm.filters[field.key]" :min="field.filter.min" :max="field.filter.max" />
                    </div>
                </div>
            </VaButtonDropdown>
        </div>
        <div class="flex">
            <VaButtonDropdown preset="primary" :closeOnContentClick="false" label="Sort" icon="sort" class="mr-2 mb-2">
                <div class="w-200">
                    <VaSelect class="mt-2" label="Sort Field" v-model="searchForm.sort_column" :options="columns" />
                    <VaSelect class="mt-2" label="Sort Order" v-model="searchForm.sort_order"
                        :options="['asc', 'desc']" />
                </div>
            </VaButtonDropdown>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref, watchEffect } from 'vue';
import { Filter, Input, Select, Range, ModelSearchForm } from '../../data/types'

const props = defineProps<{
    columns: string[],
    fields: Filter[],
}>()

onMounted(() => {
    searchForm.value.filters = { ...createFilters(props.fields) }
})

const searchForm = ref<ModelSearchForm>({
    filters: {},
    sort_column: '',
    sort_order: 'asc'
})

const emits = defineEmits(['onFilterChange', 'onShowFieldChange'])

const showFields = ref(props.fields.map((filter: Filter) => {
    return {
        show: filter.required,
        value: filter.key
    }
}))


watchEffect(() => {
    emits('onShowFieldChange', showFields.value)
})

watchEffect(() => {
    emits('onFilterChange', searchForm.value)
})

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
.w-200 {
    max-width: 350px;
}
</style>