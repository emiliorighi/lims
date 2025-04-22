<template>
    <VaModal hide-default-actions close-button v-model="userStore.showForm">
        <template #header>
            <h3 class="va-h3">
                {{ title }}
            </h3>
        </template>
        <div class="layout va-gutter-5">
            <VaForm ref="userForm">
                <div class="row align-end">
                    <div v-if="!nameToUpdate" class="flex lg6 md6 sm12 xs12">
                        <DebounceInput :loading="isInputLoading" @change="validateUsername"
                            :parent-model="userStore.userForm.name" label="Name" placeholder="Type a name..."
                            :rules="nameRules" />
                    </div>
                    <div class="flex lg6 md6 sm12 xs12">
                        <VaInput placeholder="Type a password.." :rules="passwordRules"
                            v-model="userStore.userForm.password" label="Password" />
                    </div>
                </div>
                <div class="row align-end">
                    <div class="flex lg6 md6 sm12 xs12">
                        <VaSelect v-model="userStore.userForm.role" :options="roles" label="Role">
                        </VaSelect>
                    </div>
                    <div v-if="userStore.userForm.role !== 'admin'" class="flex lg6 md6 sm12 xs12">
                        <VaSelect
                            :rules="[(v: any) => userStore.userForm.projects.length > 0 || 'Select at least one project for the user']"
                            multiple @update:search="handleSearch" v-model="userStore.userForm.projects"
                            :options="projects" placeholder="Search projects" clearable :loading="selectLoading"
                            searchable highlight-matched-text searchPlaceholderText="Type to search"
                            noOptionsText="No project found">
                        </VaSelect>
                    </div>
                </div>
            </VaForm>
        </div>

        <template #footer>
            <div class="row justify-end">
                <div class="flex">
                    <VaButton :loading="isLoading" @click="submit">Submit</VaButton>
                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, onMounted, ref } from 'vue';
import { useToast, useForm } from 'vuestic-ui/web-components';
import { useUserStore } from '../../stores/user-store'
import ProjectService from '../../services/clients/ProjectService'
import AuthService from '../../services/clients/AuthService'
import DebounceInput from '../inputs/DebounceInput.vue';

const roles = ['admin', 'project_manager']

const { init } = useToast()
const userStore = useUserStore()
const { validate } = useForm('userForm')

const nameToUpdate = computed(() => userStore.nameToUpdate)
const title = computed(() => userStore.nameToUpdate ? `Updating ${nameToUpdate.value}` : 'User form')
const projects = ref<string[]>([])
const selectLoading = ref(false)
const nameAlreadyExists = ref(false)
const isLoading = ref(false)
const isInputLoading = ref(false)
// Computed Properties
const nameRules = computed(() => {
    return [(v: string) => v.length > 0 || 'Name is mandatory', (v: string) =>
        !nameAlreadyExists.value || `User name already exists`]
})

const passwordRules = computed(() => {
    return [(v: string) => v.length > 0 || 'Password is mandatory']
})

onMounted(() => {
    if (nameToUpdate.value) projects.value = [...userStore.userForm.projects]
})

async function validateUsername(name: string) {
    userStore.userForm.name = name
    try {
        isInputLoading.value = true
        const { data } = await AuthService.getUser(name)
        nameAlreadyExists.value = true
    } catch (error) {
        const axiosError = error as AxiosError;
        if (axiosError.response && axiosError.response.status === 404) {
            // set project id
            nameAlreadyExists.value = false
        } else {
            console.error('Error fetching:', error);
            init({ message: 'Error fetching: ' + error, color: 'danger' })
        }
    } finally {
        isInputLoading.value = false
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
        const response = nameToUpdate.value
            ? await AuthService.updateUser(nameToUpdate.value, { projects, role })
            : await AuthService.createUser(userStore.userForm);

        userStore.toast({
            color: 'success',
            message: Array.isArray(response.data)
                ? response.data.join(', ')
                : ` ${nameToUpdate.value ? `${nameToUpdate.value} edited` : 'created'} successfully`,
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

async function resetForm() {
    userStore.resetUserForm();
    userStore.resetSearchForm()
    userStore.showForm = false;
    await userStore.fetchUsers({})
}
</script>