<template>
    <div>
        <VaButton icon="book" @click="triggerGet" color="info" :loading="isLoading">
            Load Draft
        </VaButton>
        <VaModal v-model="show" hide-default-actions>
            <template #header>
                <h2 class="va-h2"> Draft Projects</h2>
            </template>
            <VaDivider/>
            <div class="row align-end justify-space-between">
                <VaInput class="flex lg6 md6 sm12 xs12" @update:modelValue="getDraftProjects(query)"
                    v-model="query.filter" label="Search" placeholder="Type to search a draft project"></VaInput>
                <Pagination class="flex" @offset-changed="handlePagination" :limit="query.limit"
                    :offset="query.offset" :total="total" />
                <VaDataTable class="flex lg12 md12 sm12 xs12" :items="draftProjects"
                    :columns="['name', 'version', 'actions']">
                    <template #cell(actions)="{ row, isExpanded, rowData }">
                        <VaButton size="small" :icon="isExpanded ? 'va-arrow-up' : 'va-arrow-down'"
                            @click="row.toggleRowDetails()"> View Details
                        </VaButton>
                        <VaButton size="small" style="margin-left: 3px;" @click="setDraftProject(rowData as SchemaForm)" color="success">Use this Draft
                            Project
                        </VaButton>
                    </template>
                    <template #expandableRow="{ rowData }">
                        <ProjectOverviewCard :metadata="rowData" />
                    </template>
                </VaDataTable>
            </div>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useGlobalStore } from './../../stores/global-store';
import ProjectService from './../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import { SchemaForm } from './../../data/types';
import { useProjectStore } from './../../stores/project-store';
import ProjectOverviewCard from './../../components/project/ProjectOverviewCard.vue';
import Pagination from './../../components/filters/Pagination.vue';

const { toast } = useGlobalStore()

const draftProjects = ref<SchemaForm[]>([])

const projectStore = useProjectStore()

const isLoading = ref(false)

const show = ref(false)

const total = ref(0)

const query = reactive({
    filter: '',
    sort_order: '',
    offset: 0,
    limit: 10
})

async function triggerGet() {
    await getDraftProjects(query)
    show.value = !show.value
}


async function getDraftProjects(query: Record<string, any>) {
    try {
        isLoading.value = !isLoading.value
        const { data } = await ProjectService.getDraftProjects(query)
        draftProjects.value = [...data.data]
        total.value = data.total
    } catch (e) {
        const axiosError = e as AxiosError
        toast({ color: 'danger', message: `${axiosError.message}`, title: 'Error while fetching draft projects', duration: 1500 })
    } finally {
        isLoading.value = !isLoading.value
    }
}

function handlePagination(value: number) {
    query.offset = value - 1
    getDraftProjects({ ...query })
}

function setDraftProject(project: SchemaForm) {
    projectStore.incomingProject = { ...project }
    projectStore.draftProjectExists = !projectStore.draftProjectExists
    projectStore.confirmOverwrite = !projectStore.confirmOverwrite
    show.value = !show.value

}
</script>