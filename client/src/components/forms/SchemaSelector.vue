<template>
    <va-card>
        <va-card-title>
            Schemas
        </va-card-title>
        <va-card-content> Total: {{ total }} </va-card-content>
        <va-skeleton v-if="isLoading" height="400px" />
        <va-card-content v-else-if="errorMessage">
            {{ errorMessage }}
        </va-card-content>
        <va-card-content v-else>
            <SearchForm @on-submit="handleSubmit" @on-reset="reset" :filters="filters"
                :search-form="schemaStore.searchForm"></SearchForm>
            <va-data-table :items="schemas" :columns="['name', 'description', 'version', 'action']">
                <template #cell(action)="{ rowData }">
                    <va-button @click="useSchema(rowData)">
                        Select schema
                    </va-button>
                </template>
            </va-data-table>
            <div class="row align-center justify-center">
                <div class="flex">
                    <va-pagination v-model="offset" :page-size="schemaStore.pagination.limit" :total="total"
                        :visible-pages="3" buttons-preset="secondary" rounded gapped border-color="primary"
                        @update:model-value="handlePagination" />
                </div>
            </div>
        </va-card-content>
    </va-card>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store'
import { ref } from 'vue'
import ProjectService from '../../services/clients/ProjectService'
import SearchForm from './SearchForm.vue'
import { Filter } from '../../data/types'

const schemaStore = useSchemaStore()
const offset = ref(1 + schemaStore.pagination.offset)
const schemas = ref([])
const total = ref(0)
const isLoading = ref(false)
const errorMessage = ref('')
const filters: Filter[] = [
    {
        label: 'filter',
        type: {
            name: 'input',
            type: 'string'

        },
        key: 'filter',
        required: true,
        value: ''
    },
    {
        label: 'sort order',
        type: {
            name: 'select',
            type: 'single',
            choices: ['asc', 'desc']

        },
        key: 'sort_order',
        required: false,
        value: '',
    }
]
await getSchemas({ ...schemaStore.pagination, ...schemaStore.searchForm })

async function getSchemas(query: Record<string, any>) {
    try {
        const { data } = await ProjectService.getProjects(query)
        schemas.value = data.data
        total.value = data.total
    } catch {
        errorMessage.value = 'Something happened'
    } finally {
        isLoading.value = false
    }
}
async function handleSubmit() {
    schemaStore.resetPagination()
    offset.value = 1
    getSchemas({ ...schemaStore.searchForm, ...schemaStore.pagination })
}
async function handlePagination(value: number) {
    schemaStore.pagination.offset = value - 1
    getSchemas({ ...schemaStore.searchForm, ...schemaStore.pagination })
}
async function reset() {
    offset.value = 1
    schemaStore.resetSeachForm()
    schemaStore.resetPagination()
    getSchemas({ ...schemaStore.pagination })
}
function useSchema(schema:Record<string,any>) {
    schemaStore.schema = {...schema}
}
</script>
