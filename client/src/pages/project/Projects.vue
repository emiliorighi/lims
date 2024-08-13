<template>
    <h1 class="va-h1">Projects</h1>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex">
                            <VaInput v-model="searchForm.filter" placeholder="Search project" clearable>
                                <template #appendInner>
                                    <VaIcon name="search" />
                                </template>
                            </VaInput>
                        </div>
                        <div class="flex">
                            <VaButton :to="{ name: 'project-form' }" icon="add">
                                Project
                            </VaButton>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <VaDataTable :items="projects" :columns="['name', 'description', 'version', 'action']">
                        <template #cell(action)="{ rowData }">
                            <VaChip size="small" square @click="useProject(rowData as SchemaForm)">
                                View details
                            </VaChip>
                        </template>
                    </VaDataTable>
                </VaCardContent>
                <VaCardContent>
                    <Pagination @offset-changed="handlePagination" :limit="searchForm.limit" :offset="searchForm.offset"
                        :total="total" />
                </VaCardContent>
            </VaCard>
        </div>
    </div>

</template>
<script setup lang="ts">
import { reactive, ref, watchEffect } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import { useRouter } from 'vue-router';
import { useSchemaStore } from '../../stores/schemas-store';
import { SchemaForm } from '../../data/types';
import Pagination from '../../components/filters/Pagination.vue';

const projects = ref<Record<string, any>[]>([])
const router = useRouter()
const schemaStore = useSchemaStore()
const isLoading = ref(false)

const searchForm = reactive({
    offset: 0,
    filter: '',
    limit: 10
})
const total = ref(0)

watchEffect(async () => {
    await getProjects(searchForm)
})

function useProject(project: SchemaForm) {
    schemaStore.schema = { ...project }
    router.push({ name: 'project', params: { projectId: project.project_id } })
}

async function getProjects(params: Record<string, any>) {
    if (params.offset > 1) params.offset = params.offset - 1
    try {
        isLoading.value = true
        const { data } = await ProjectService.getProjects(params)
        projects.value = data.data
        total.value = data.total
    } catch (error) {
        console.error(error)

    } finally {
        isLoading.value = false
    }
}

function handlePagination(v: number) {
    searchForm.offset = v - 1
}

</script>