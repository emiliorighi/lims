<template>
    <div class="row align-center">
        <div class="flex flex-grow">
            <VaBadge :text="field.isIdField?'ID':''" color="warning" overlap placement="top-start">
                <span>{{ field.key }}</span>
            </VaBadge>
            <VaIcon @click="sortItems(field.key)" style="margin-left: 3px;cursor: pointer;" color="textPrimary"
                :name="recordStore.sort.sort_column === field.key ? sortIcons[sortStep] : 'swap_vert'"></VaIcon>
            <VaBadge :dot="Object.values(field.payload).filter(Boolean).length > 0" overlap color="info">
                <VaButtonDropdown stick-to-edges :close-on-content-click="false" size="small" preset="secondary"
                    color="textPrimary" icon="fa-filter">
                    <div class="layout va-gutter-3" style="max-width: 200px;">
                        <DynamicFilterField :key="field.key" :field="field" :model-name="modelName"
                            :project-id="projectId" @update-query="debounceSearchFormUpdate">
                        </DynamicFilterField>
                    </div>
                </VaButtonDropdown>
            </VaBadge>
        </div>
        <!-- <div class="flex">
            <VaBadge :dot="Object.values(field.payload).filter(Boolean).length > 0" overlap color="info">
                <VaButtonDropdown stick-to-edges :close-on-content-click="false" size="small" preset="secondary"
                    color="textPrimary" icon="fa-filter">
                    <div class="layout va-gutter-3" style="max-width: 200px;">
                        <DynamicFilterField :key="field.key" :field="field" :model-name="modelName"
                            :project-id="projectId" @update-query="debounceSearchFormUpdate">
                        </DynamicFilterField>
                    </div>
                </VaButtonDropdown>
            </VaBadge>
        </div> -->
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import DynamicFilterField from '../filters/DynamicFilterField.vue';
import { QueryOperator } from '../../data/types';
import { useRecordStore } from '../../stores/record-store';
import { debounce } from '../../composables/debounce';

const props = defineProps<{
    projectId: string,
    modelName: string,
    field: { key: string, type: string, payload: any, choices?: string[], isIdField?: boolean },
}>()

const sortIcons = ['arrow_downward', 'arrow_upward', 'swap_vert']
const sortSteps = ['asc', 'desc', null]


const sortStep = ref(sortSteps.lastIndexOf(null))
const recordStore = useRecordStore()



async function handleUpdate(payload: { key: string, query: Record<QueryOperator, any> }) {
    const { key, query } = payload
    recordStore.searchForm[key] = { ...query }
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.modelName)
}

const debounceSearchFormUpdate = debounce((payload: { key: string, query: Record<QueryOperator, any> }) => {
    handleUpdate(payload)
}, 500);

async function sortItems(columnKey: string) {
    if (recordStore.sort.sort_column === columnKey) {
        sortStep.value = sortStep.value + 1 >= sortSteps.length ? 0 : sortStep.value + 1
    } else {
        sortStep.value = 0
        recordStore.sort.sort_column = columnKey
    }
    recordStore.sort.sort_order = sortSteps[sortStep.value]
    await recordStore.fetchRecords(props.projectId, props.modelName)
}


</script>
<style>
.m-w-250 {
    min-width: 250px;
}
</style>