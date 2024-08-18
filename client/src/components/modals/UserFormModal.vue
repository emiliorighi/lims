<template>
    <VaModal @cancel="resetForm" hide-default-actions max-height="500px" fixed-layout v-model="userStore.showForm">
        <template #header>
            <Header :title="userStore.user?.name ? `Update ${userStore.user.name}` : 'Create User'" />
        </template>
        <VaDivider />
        <VaInnerLoading :loading="userStore.isLoading">
            <VaForm ref="userForm">
                <div v-if="!isUpdate" class="row align-end">
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaInput label="Name" :rules="nameRules" placeholder="Type a name.."
                            v-model="userStore.userForm.name" />
                    </div>
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaInput placeholder="Type a password.." :rules="passwordRules"
                            v-model="userStore.userForm.password" label="Password" />
                    </div>
                </div>
                <div class="row align-end">
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaSelect v-model="userStore.userForm.role" :options="roles" label="Role">
                        </VaSelect>
                    </div>
                    <div class="flex lg6 md6 sm12 xs12 p-6">
                        <VaSelect :disabled="userStore.userForm.role === 'admin'" multiple @update:search="handleSearch"
                            v-model="userStore.userForm.projects" :options="projects" placeholder="Search projects"
                            clearable :loading="selectLoading" searchable highlight-matched-text
                            searchPlaceholderText="Type to search" noOptionsText="No project found">
                        </VaSelect>
                    </div>
                </div>
            </VaForm>
        </VaInnerLoading>
        <template #footer>
            <div class="row justify-end">
                <div class="flex">
                    <VaButton @click="submit">Submit</VaButton>
                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref, watch } from 'vue';
import { useToast, useForm } from 'vuestic-ui/web-components';
import { useUserStore } from '../../stores/user-store'
import ProjectService from '../../services/clients/ProjectService'
import AuthService from '../../services/clients/AuthService'
import Header from './common/Header.vue'

const roles = ['admin', 'project_manager']

const { init } = useToast()
const userStore = useUserStore()
const { validate } = useForm('userForm')

const projects = ref<string[]>([])
const selectLoading = ref(false)
const nameAlreadyExists = ref(false)
// Computed Properties
const nameRules = computed(() => {
    return [(v: string) => v.length > 0 || 'Name is mandatory',
    !nameAlreadyExists.value || `User name already exists`]
})

const passwordRules = computed(() => {
    return [(v: string) => v.length > 0 || 'Password is mandatory']
})

const isUpdate = computed(() => {
    return !!userStore.user
})

// Watchers
watch(() => (userStore.userForm.name), async (v) => {
    if (isUpdate.value) return
    await getUser(v)
})
// Methods

async function getUser(name: string) {
    try {
        const { data } = await AuthService.getUser(name);
        if (data) {
            init({ message: `User with ${name} already exists`, color: 'danger' });
            nameAlreadyExists.value = true
        }
    } catch (error) {
        if (error instanceof AxiosError && error.response?.status === 404) {
            nameAlreadyExists.value = false
        } else {
            handleError(error, 'Error fetching item');
            nameAlreadyExists.value = true
        }
    }
}
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

async function submit() {
    if (!validate()) return;
    userStore.isLoading = true;

    const { projects, role } = userStore.userForm
    try {
        const response = isUpdate.value
            ? await AuthService.updateUser(userStore.user?.name, { projects, role })
            : await AuthService.createUser(userStore.userForm);

        userStore.toast({
            color: 'success',
            message: Array.isArray(response.data)
                ? response.data.join(', ')
                : ` ${isUpdate.value ? `${userStore.user?.name} edited` : 'created'} successfully`,
        });

        resetForm();
    } catch (error) {
        handleError(error, 'Error saving item');
    } finally {
        userStore.isLoading = false;
    }
}

function handleError(error: any, defaultMessage: string) {
    console.error(defaultMessage, error);
    const message = error instanceof AxiosError ? error.response?.data?.message || defaultMessage : defaultMessage;
    userStore.toast({ color: 'danger', message });
}

function resetForm() {
    userStore.resetUserForm();
    userStore.resetSearchForm()
    userStore.user = undefined
    userStore.fetchUsers();
    userStore.showForm = false;
}
</script>