<template>
    <div class="row justify-space-between">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput v-model="filter" @update:model-value="debouncedSearch" placeholder="Search by indentifier"
                clearable>
                <template #appendInner>
                    <VaButton style="margin-left: 3px;" preset="secondary" color="textPrimary" icon="help"
                        @click="showQueryInfo = !showQueryInfo" />
                </template>
            </VaInput>
        </div>
    </div>
    <VaModal v-model="showQueryInfo">
        <template #header>
            <h3 class="va-h3">
                Record identifier filter
            </h3>
            <p class="va-text-secondary">This input filters by the formatted identifier of {{ model.name }} that is
                composed by
                the
                following fields:</p>
        </template>
        <div class="layout va-gutter-3 fluid">
            <div class="row">
                <div v-for="idField in model.id_format" :key="idField" class="flex">
                    <VaChip color="textPrimary">{{ idField }}</VaChip>
                </div>
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRecordStore } from '../../../stores/record-store';
import { ReseachModel } from '../../../data/types';
import { debounce } from '../../../composables/debounce';


const props = defineProps<{
    projectId: string,
    model: ReseachModel
}>()

const emits = defineEmits(['search'])

const recordStore = useRecordStore()
const showQueryInfo = ref(false)


const filter = computed({
    get() {
        return recordStore.searchForm.filter?.filter ?? ""
    }, set(filter: string) {
        recordStore.searchForm.filter = { filter }
    }
})

async function handleSearch(filter: string) {
    recordStore.searchForm.filter = { filter }
    recordStore.resetPagination()
    await recordStore.fetchRecords(props.projectId, props.model.name)
}

const debouncedSearch = debounce(async (payload: any) => {
    await handleSearch(payload)

}, 200);


</script>