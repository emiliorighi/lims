<template>
    <Header :title="title" />
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex">
                            <div class="row">
                                <div class="flex">
                                    <VaInput v-model="userStore.searchForm.filter" placeholder="Search User" clearable>
                                        <template #appendInner>
                                            <VaIcon name="search" />
                                        </template>
                                    </VaInput>
                                </div>
                                <div class="flex">
                                    <VaSelect @update:search="handleSearch" v-model="userStore.searchForm.project"
                                        :options="projects" placeholder="Search projects" clearable
                                        :loading="selectLoading" searchable highlight-matched-text
                                        searchPlaceholderText="Type to search" noOptionsText="No project found">
                                    </VaSelect>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <VaButton @click="createUser" icon="add">User</VaButton>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <VaDataTable :loading="isLoading" :items="userStore.users"
                        :columns="['name', 'projects', 'role', 'actions']">
                        <template #cell(actions)="{ rowData }">
                            <VaButton @click="editUser(rowData)" preset="plain" icon="edit" />
                            <VaButton preset="plain" icon="delete" color="danger" class="ml-3" />
                        </template>
                    </VaDataTable>
                </VaCardContent>
                <VaCardContent>
                    <Pagination @offset-changed="handlePagination" :limit="userStore.searchForm.limit"
                        :offset="userStore.searchForm.offset" :total="userStore.total" />
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <UserFormModal />
</template>
<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import ProjectService from '../../services/clients/ProjectService'
import { AxiosError } from 'axios'
import Pagination from '../../components/filters/Pagination.vue';
import Header from '../../components/ui/Header.vue'
import { useToast } from 'vuestic-ui'
import UserFormModal from '../../components/modals/UserFormModal.vue'
import { User } from '../../data/types'
import { useUserStore } from '../../stores/user-store'

const userStore = useUserStore()

const props = defineProps<{
    title: string
}>()

const { init } = useToast()
const selectLoading = ref(false)
const isLoading = ref(false)
const projects = ref<string[]>([])

watch(() => userStore.searchForm, async () => {
    await userStore.fetchUsers()
})

onMounted(async () => {
    await userStore.fetchUsers()

})
async function handleSearch(query: string) {
    if (query.length < 2) return;
    selectLoading.value = true;

    try {
        const { data } = await ProjectService.getProjects({ filter: query });
        projects.value = [...data.data.map((i: any) => i.project_id)]
    } catch (error) {
        handleError(error, 'Error fetching projects');
    } finally {
        selectLoading.value = false;
    }
}

function handleError(error: any, defaultMessage: string) {
    console.error(defaultMessage, error);
    const message = error instanceof AxiosError ? error.response?.data?.message || defaultMessage : defaultMessage;
    init({ color: 'danger', message });
}

function handlePagination(v: number) {
    userStore.searchForm.offset = v - 1
}

function createUser() {
    userStore.resetUserForm()
    userStore.showForm = !userStore.showForm
}

function editUser(rowData: User) {
    userStore.user = { ...rowData }
    userStore.userForm = { ...rowData }
    userStore.showForm = !userStore.showForm
}
</script>