<template>
    <VaCard>
        <VaCardContent>
            <div class="row justify-space-between align-center">
                <div class="flex">
                    <div class="row">
                        <div class="flex">
                            <ItemsInput :model="model" @value-change="handleSearch" />
                        </div>
                        <div v-if="hasFilters" class="flex">
                            <TableFilters :fields="filters" :project-id="project_id" />
                        </div>
                        <div class="flex">
                            <VaButton :disabled="itemStore.stores[model].total === 0" preset="primary"
                                @click="itemStore.showReport = !itemStore.showReport" icon="download">
                                Report
                            </VaButton>
                        </div>
                        <div v-if="isAuthorized" class="flex">
                            <VaButton icon="add" @click="newItem">
                                {{ buttonLabel }}
                            </VaButton>
                        </div>
                    </div>
                </div>
                <div class="flex">
                    <h4 class="va-h4">
                        {{ total }}
                        <span style="text-transform: capitalize">
                            {{ model }}s
                        </span>
                    </h4>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <ItemsTable :isAuthorized="isAuthorized" :project-id="project_id" :items="itemStore.stores[model].items"
                :filters="filters" />
            <Pagination @offset-changed="handlePagination" :limit="limit" :offset="offset" :total="total" />
        </VaCardContent>
    </VaCard>

</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue';
import { useSchemaStore } from '../../../stores/schemas-store'
import TableFilters from '../../../components/filters/TableFilters.vue'
import { ModelType } from '../../../data/types';
import Pagination from '../../../components/filters/Pagination.vue'
import { useItemStore } from '../../../stores/item-store'
import ItemsTable from '../../../components/tables/ItemsTable.vue'
import ItemsInput from '../../../components/inputs/ItemsInput.vue';
import { useGlobalStore } from '../../../stores/global-store';

const itemStore = useItemStore()
const schemaStore = useSchemaStore()
const globalStore = useGlobalStore()
const { project_id } = schemaStore.schema

const props = defineProps<{
    model: ModelType,
    buttonLabel: string,
    icon: string
}>()


watch(() => props.model, async () => {
    itemStore.resetSearchForm()
    itemStore.resetPagination()
    itemStore.currentModel = props.model
    await itemStore.fetchItems(schemaStore.schema.project_id)
})

onMounted(async () => {
    itemStore.currentModel = props.model
    await itemStore.fetchItems(schemaStore.schema.project_id)
})

onUnmounted(() => {
    itemStore.resetSearchForm()
    itemStore.resetPagination()
})

const isAuthorized = computed(() => {
    return globalStore.isAuthenticated && (globalStore.user.role === 'admin' || globalStore.user.projects.includes(schemaStore.schema.project_id))
})
const offset = computed(() => {
    const m = itemStore.currentModel
    return itemStore.stores[m].pagination.offset
})

const limit = computed(() => {
    const m = itemStore.currentModel
    return itemStore.stores[m].pagination.limit
})
const total = computed(() => {
    const m = itemStore.currentModel
    return itemStore.stores[m].total
})

async function handleSearch(payload: { field: 'sample_id' | 'experiment_id', value: string }) {
    const { field, value } = payload
    const m = itemStore.currentModel
    itemStore.stores[m].searchForm[field] = value
    await itemStore.fetchItems(project_id)
}

const filters = computed(() => schemaStore.schema[props.model].fields)

const hasFilters = computed(() => schemaStore.schema[props.model].id_format.length < schemaStore.schema[props.model].fields.length)
async function handlePagination(offset: number) {
    const m = itemStore.currentModel
    itemStore.stores[m].pagination.offset = offset - 1;
    await itemStore.fetchItems(project_id)
}

function newItem() {
    const m = itemStore.currentModel
    itemStore.stores[m].item = null
    itemStore.showForm = !itemStore.showForm;
}


</script>