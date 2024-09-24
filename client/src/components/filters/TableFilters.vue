<template>
    <VaBadge style="z-index: 1;" overlap color="info" :text="activeFilters">
        <VaButtonDropdown :closeOnContentClick="false" icon="tune" label="Filters" preset="primary">
            <div class="row row-drop-down">
                <div class="flex" v-for="(field, index) in fields" :key="index">
                    <TextInput class="mt-3" @value-change="(v) => updateQuery(v, field)" :label="field.label"
                        :type="field.filter.input_type" v-if="isInputField(field.filter)"
                        :value="searchForm[field.key]">
                    </TextInput>
                    <SelectInput class="mt-3" @value-change="(v) => updateQuery(v, field)"
                        :options="field.filter.choices" :multi="field.filter.multi" :label="field.label"
                        :value="searchForm[field.key]" v-else-if="isSelectField(field.filter)"></SelectInput>
                    <!-- <RangeInput @value-change="(v) => updateQuery(v, field)" :label="field.label" :min="field.filter.min"
                :max="field.filter.max" v-else-if="isRangeField(field.filter)"></RangeInput> -->
                </div>
            </div>
        </VaButtonDropdown>
    </VaBadge>

</template>
<script setup lang="ts">
import { Filter, Input, Select, Range } from '../../data/types'
import TextInput from '../inputs/Input.vue'
import SelectInput from '../inputs/Select.vue'
import { useItemStore } from '../../stores/item-store';
import { computed } from 'vue';

const props = defineProps<{
    fields: Filter[],
    projectId: string
}>()

const itemStore = useItemStore()

const activeFilters = computed(() => {
    const m = itemStore.currentModel
    return Object.entries(itemStore.stores[m].searchForm).filter(([k, v]) => v && k !== 'sample_id' && k !== 'experiment_id').length
})

const searchForm = computed(() => itemStore.stores[itemStore.currentModel].searchForm)

async function updateQuery(v: any, field: Filter) {
    const m = itemStore.currentModel
    const { filter, key } = field
    if (isInputField(filter)) {
        itemStore.stores[m].searchForm[key] = v
    } else if (isSelectField(filter)) {
        let value = filter.multi ? v.join(', ') : v
        itemStore.stores[m].searchForm[key] = value
    } else {
        const [min, max] = v
        itemStore.stores[m].searchForm[`${key}__lte`] = max
        itemStore.stores[m].searchForm[`${key}__gte`] = min
    }
    itemStore.resetPagination()
    await itemStore.fetchItems(props.projectId)
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
    max-height: 400px;
    max-width: min-content;
    overflow: scroll;
    padding: 16px;
}
.mt-3{
    margin-top: 3px;
}
</style>
