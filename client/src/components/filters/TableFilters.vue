<template>
    <div class="row">
        <div class="flex">
            <VaInput iconColor="primary" v-model="filter" clearable
                @update:modelValue="(v: string) => emits('onFormChange', [['filter', v.length > 2 ? v : '']])"
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
        <div class="flex">
            <VaButtonDropdown :closeOnContentClick="false" icon="filter_list" label="Filters" preset="primary"
                class="mr-2 mb-2">
                <div class="row row-drop-down">
                    <div class="flex lg12 md12 sm12 xs12" v-if="searchForm.filters" v-for="(field, index) in fields"
                        :key="index">
                        <VaInput @update:modelValue="(v: string) => emits('onFormChange', [[field.key, v]])"
                            class="mt-2" clearable :label="field.key" v-if="isInputField(field.filter)"
                            v-model="searchForm.filters[field.key]">
                        </VaInput>
                        <VaSelect class="mt-2"
                            @update:modelValue="(v: string) => emits('onFormChange', [[field.key, v]])" clearable
                            :label="field.key" v-else-if="isSelectField(field.filter)"
                            v-model="searchForm.filters[field.key]" :multiple="field.filter.multi"
                            :options="field.filter.choices">
                        </VaSelect>

                        <VaSlider label="Age range" v-else-if="isRangeField(field.filter)"
                            @update:modelValue="(v: string) => emits('onFormChange', [[field.key, v]])"
                            v-model="searchForm.filters[field.key]" class="mt-4" :min="field.filter.min"
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
        </div>
        <div class="flex">
            <VaButtonDropdown preset="primary" :closeOnContentClick="false" label="Sort" icon="sort" class="mr-2 mb-2">
                <div class="row row-drop-down">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaSelect class="mt-2" label="Sort Field"
                            @update:modelValue="(v: string) => emits('onFormChange', [['sort_column', v]])"
                            v-model="searchForm.sort_column" :options="columns" />
                    </div>
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaSelect class="mt-2" label="Sort Order"
                            @update:modelValue="(v: string) => emits('onFormChange', [['sort_order', v]])"
                            v-model="searchForm.sort_order" :options="['asc', 'desc']" />
                    </div>
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

const filter = ref('')

onMounted(() => {
    searchForm.value.filters = { ...createFilters(props.fields) }
})

const searchForm = ref<ModelSearchForm>({
    filters: {},
    sort_column: '',
    sort_order: 'asc'
})

const emits = defineEmits(['onFormChange', 'onShowFieldChange'])

const showFields = ref(props.fields.map((filter: Filter) => {
    return {
        show: filter.required,
        value: filter.key
    }
}))


watchEffect(() => {
    emits('onShowFieldChange', showFields.value)
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
.row-drop-down {
    width: min-content;
    max-height:400px;
    overflow: scroll;
    padding: 16px;
}
</style>
