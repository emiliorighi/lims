<template>
    <div>
        <div class="row align-end justify-space-between">
            <div class="flex">
                <h1 class="va-h1">Projects</h1>
                <p class="va-text-secondary">
                    List of projects
                </p>
            </div>
        </div>
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <VaCard>
                    <VaCardContent>
                        <div class="row align-center justify-space-between">
                            <div class="flex">
                                <div class="row">
                                    <div class="flex">
                                        <VaButtonGroup>
                                            <VaButton :preset="searchForm.archived == opt.value?undefined:'primary'"  @click="searchForm.archived = opt.value"
                                                :key="opt.label" v-for="opt in options">
                                                {{ opt.label }}
                                            </VaButton>
                                        </VaButtonGroup>
                                    </div>
                                    <div class="flex">
                                        <VaInput v-model="searchForm.filter" placeholder="Search project" clearable>
                                        </VaInput>
                                    </div>
                                </div>
                            </div>
                            <div class="flex">
                                <VaButton :to="{ name: 'project-form' }" icon="add">
                                    New Project
                                </VaButton>
                            </div>
                        </div>
                        <VaDataTable clickable hoverable @row:click="goToProject" :items="projects"
                            :columns="['name', 'description', 'version', 'archived']">
                            <template #cell(archived)="{ rowData }">
                                <VaChip size="small" :color="rowData.archived ? 'warning' : 'success'">
                                    {{ rowData.archived ? 'archived' : 'active' }}
                                </VaChip>
                            </template>
                        </VaDataTable>
                    </VaCardContent>
                    <VaCardContent>
                        <div class="row justify-space-between align-center">
                            <div class="flex">
                                Results: {{ total }}
                            </div>
                            <div class="flex">
                                <div class="row justify-center">
                                    <div class="flex">
                                        <VaPagination v-model="offset" :page-size="limit" :total="total"
                                            :visible-pages="3" buttons-preset="primary" gapped />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </VaCardContent>
                </VaCard>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, reactive, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useProjectStore } from '../stores/project-store';

const options = [
    { label: 'Active', value: false },
    { label: 'Inactive', value: true }
]

const router = useRouter()
const projectStore = useProjectStore()
const limit = 10
const searchForm = reactive({
    offset: 0,
    filter: '',
    limit: 10,
    archived: false,
})

const offset = computed({
    get() {
        return searchForm.offset + 1
    }, set(v: number) {
        searchForm.offset = v - 1
    }
})

const total = computed(() => projectStore.total)
const projects = computed(() => projectStore.projects)

async function goToProject(payload: any) {
    const { row } = payload
    const projectId = row.rowData.project_id
    await projectStore.getProjectSchema(projectId)
    router.push({ name: 'project', params: { projectId } })
}

watch(() => searchForm, async () => {
    await projectStore.getProjects(searchForm)
}, { immediate: true, deep: true })



</script>