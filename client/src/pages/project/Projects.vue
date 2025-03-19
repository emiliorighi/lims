<template>
    <Header :title="title" />
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <div class="row align-center justify-space-between">
                        <div class="flex">
                            <div class="row align-center">
                                <div class="flex">
                                    <VaInput v-model="searchForm.filter" placeholder="Search project" clearable>
                                        <template #appendInner>
                                            <VaIcon name="search" />
                                        </template>
                                    </VaInput>
                                </div>
                                <div v-if="isProjectManager" class="flex">
                                    <VaButtonToggle preset="secondary" border-color="primary" v-model="viewAll"
                                        :options="viewOptions" />
                                </div>
                            </div>
                        </div>
                        <div v-if="isAdmin" class="flex">
                            <VaButton :to="{ name: 'project-form' }" icon="add">
                                Project
                            </VaButton>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <VaDataTable :items="projects" :columns="['name', 'description', 'version', 'action']">
                        <template #cell(action)="{ rowData }">
                            <VaChip size="small" square @click="useProject(rowData as ReseachProject)">
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
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useSchemaStore } from '../../stores/schema-store';
import Pagination from '../../components/filters/Pagination.vue';
import Header from '../../components/ui/Header.vue'
import { useGlobalStore } from '../../stores/global-store'
import { ReseachProject } from '../../data/types';
import ProjectService from '../../services/clients/ProjectService';

const globalStore = useGlobalStore()
const props = defineProps<{
    title: string
}>()
const viewOptions = [
    { label: "My Projects", value: false },
    { label: "All Projects", value: true },
]
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
const viewAll = ref(false)

const isAdmin = computed(() => {
    return globalStore.user.role === 'admin'
})

const isProjectManager = computed(() => {
    return globalStore.user.role === 'project_manager'
})

watch(() => searchForm, async () => {
    await getProjects(searchForm)
}, { deep: true })

watch(() => viewAll.value, async () => {
    await getProjects(searchForm)
}, { deep: true })

onMounted(async () => {
    await getProjects(searchForm)
})

function useProject(project: ReseachProject) {
    router.push({ name: 'projectSchema', params: { projectId: project.project_id } })
}

async function getProjects(params: Record<string, any>) {
    if (params.offset > 1) params.offset = params.offset - 1
    const query = { ...params }
    try {
        isLoading.value = true
        const { data } = isProjectManager.value && !viewAll.value ?
            await ProjectService.getUserProjects(globalStore.user.name, query) :
            await ProjectService.getProjects(query)
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