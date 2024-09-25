import { defineStore } from 'pinia'
import { User } from '../data/types'
import AuthService from '../services/clients/AuthService'
import { useToast } from 'vuestic-ui/web-components'

const initSearchForm = {
    offset: 0,
    filter: '',
    project: '',
    limit: 10
}

const initForm: User = {
    name: '',
    password: '',
    role: 'project_manager',
    projects: []
}
export const useUserStore = defineStore('user', {
    state: () => {
        return {
            user: undefined as User | undefined,
            users: [] as User[],
            showForm: false,
            userForm: { ...initForm },
            showDetails: false,
            isLoading: false,
            searchForm: { ...initSearchForm },
            total: 0,
            toast: useToast().init,
        }
    },

    actions: {

        async fetchUsers() {
            this.isLoading = true
            try {
                const { data } = await AuthService.getUsers(this.searchForm);
                this.users = [...data.data];
                this.total = data.total;
            } catch (e) {
                this.toast({ message: 'Error fetching data', color: 'danger' })
            } finally {
                this.isLoading = false
            }

        },
        async createUser() {
            this.isLoading = true
            try {
                const { data } = await AuthService.createUser(this.userForm);
                this.toast({ message: data, color: 'success', duration: 1500 });

            } catch (e) {
                this.toast({ message: 'Error fetching data', color: 'danger' })
            } finally {
                this.isLoading = false
            }
        },
        async updateUser(id: string) {
            this.isLoading = true
            try {
                const { data } = await AuthService.updateUser(id, this.userForm);
                this.toast({ message: data, color: 'success', duration: 1500 });

            } catch (e) {
                this.toast({ message: 'Error fetching data', color: 'danger' })
            } finally {
                this.isLoading = false
            }
        },
        async deleteUser(id: string) {
            this.isLoading = true

            try {
                const { data } = await AuthService.deleteUser(id)
                this.toast({ message: data, color: 'success', duration: 1500 });
                // reset();
            } catch (error) {
                console.error(error);
                this.toast({ message: 'Error deleting item', color: 'danger', duration: 1500 });
            } finally {
                this.isLoading = false

            }
        },
        resetSearchForm() {
            this.searchForm = { ...initSearchForm }
        },
        resetUserForm() {
            this.userForm = { ...initForm }
        }
    }
})
