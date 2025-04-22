<template>
    <div>
        <div class="row align-end justify-space-between">
            <div class="flex">
                <h1 class="va-h1">Users</h1>
                <p class="va-text-secondary">
                    List of users
                </p>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex">
                            <VaInput v-model="searchForm.filter" placeholder="Search User" clearable>
                            </VaInput>
                        </div>
                        <div class="flex">
                            <VaButton @click="createUser" icon="add">New User</VaButton>
                        </div>
                    </div>
                    <VaDataTable :loading="isLoading" :items="userStore.users"
                        :columns="['name', 'projects', 'role', 'actions']">
                        <template #cell(actions)="{ rowData }">
                            <div v-if="rowData.name !== gStore.user.name">
                                <VaButton @click="editUser(rowData)" preset="plain" icon="edit" />
                                <VaButton @click="triggerDelete(rowData)" preset="plain" icon="delete" color="danger"
                                    class="ml-3" />
                            </div>
                        </template>
                        <template #cell(role)="{ rowData }">
                            <VaChip size="small" color="backgroundElement">
                                {{ rowData.role }}
                            </VaChip>
                        </template>
                    </VaDataTable>
                </VaCardContent>
                <VaCardContent>
                    <div class="row justify-center">
                        <div class="flex">
                            <VaPagination v-model="offset" :page-size="searchForm.limit" :total="total"
                                :visible-pages="3" buttons-preset="primary" gapped />
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <UserFormModal />
    <ConfirmDeleteModal @confirmDelete="deleteUser" :idToDelete="idToDelete" icon="person" />
</template>
<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue';
import UserFormModal from '../components/modals/UserFormModal.vue'
import { useUserStore } from '../stores/user-store'
import ConfirmDeleteModal from '../components/modals/ConfirmDeleteModal.vue';
import { useGlobalStore } from '../stores/global-store';

const userStore = useUserStore()
const gStore = useGlobalStore()
const isLoading = ref(false)
const idToDelete = ref('')

const initSearchForm = {
    offset: 0,
    filter: '',
    limit: 10,
}

const searchForm = reactive({ ...initSearchForm })

const total = computed(() => userStore.total)
const offset = computed({
    get() {
        return searchForm.offset + 1
    }, set(v: number) {
        searchForm.offset = v - 1
    }
})

watch(() => searchForm, async () => {
    await userStore.fetchUsers(searchForm)
}, { immediate: true, deep: true })


function triggerDelete(rowData: any) {
    idToDelete.value = rowData.name
    gStore.showDeleteConfirmation = !gStore.showDeleteConfirmation
}

function createUser() {
    userStore.resetUserForm()
    userStore.showForm = !userStore.showForm
}

function editUser(rowData: any) {
    userStore.nameToUpdate = rowData.name
    userStore.userForm = { ...rowData }
    userStore.showForm = !userStore.showForm
}

async function deleteUser() {
    await userStore.deleteUser(idToDelete.value)
    gStore.showDeleteConfirmation = !gStore.showDeleteConfirmation
    searchForm.filter = ""
    offset.value = 1
    await userStore.fetchUsers(searchForm)
}

</script>