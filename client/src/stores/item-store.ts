import { defineStore } from 'pinia'
import { ModelType } from '../data/types'
import ItemService from '../services/clients/ItemService'
import { useToast } from 'vuestic-ui/web-components'
import { AxiosError } from 'axios'
import AuthService from '../services/clients/AuthService'

const MODELS = ['sample', 'experiment']

const staticFilters = {
    sort_order: "",
    sort_column: "",
}
const initPagination = {
    offset: 0,
    limit: 10,
}

function mapModelStore() {
    const searchForm = {} as Record<string, any>
    const sort = { ...staticFilters }
    const pagination = { ...initPagination }
    const items: Record<string, any>[] = []
    const item: null | Record<string, any> = null
    const total = 0
    return {
        searchForm,
        pagination,
        sort,
        items,
        item,
        total,
    }
}

export const useItemStore = defineStore('item', {
    state: () => {
        const mappedStores = MODELS.map(m => [m, mapModelStore()])
        const stores = Object.fromEntries(mappedStores)
        return {
            showForm: false,
            showReport: false,
            isLoading: false,
            isTSVLoading: false,
            currentModel: 'sample' as ModelType,
            stores,
            showItemDetails: false,
            showDeleteConfirm: false,
            idToDelete: undefined as undefined | string,
            toast: useToast().init,
        }
    },
    actions: {
        async fetchItems(projectId: string) {
            this.isLoading = true
            const model = this.currentModel
            const { searchForm, pagination, sort } = this.stores[model]
            const params = { ...searchForm, ...pagination, ...sort }
            try {
                const { data } = await ItemService.getItems(projectId, model, params);
                this.stores[model].items = [...data.data];
                this.stores[model].total = data.total;
            } catch (e) {
                this.toast({ message: 'Error fetching data', color: 'danger' })
            } finally {
                this.isLoading = false
            }

        },
        async fetchItem(projectId: string, itemId: string) {
            this.isLoading = true
            const model = this.currentModel
            console.log(itemId)
            try {
                const { data } = await ItemService.getItem(projectId, itemId, model)
                this.stores[model].item = { ...data }
                this.showItemDetails = true
            } catch (e) {
                let message: string
                const axiosError = e as AxiosError

                if (axiosError.response?.data) {
                    message = (axiosError.response.data as { message: string }).message || axiosError.response.data as string
                } else {
                    message = axiosError.message
                }
                this.toast({ message: message, color: 'danger' })
            } finally {
                this.isLoading = false
            }
        },
        async deleteItem(projectId: string) {
            if (!this.idToDelete) return
            this.isLoading = true
            const model = this.currentModel
            try {
                const { data } = await AuthService.deleteItem(projectId, this.idToDelete, model);
                this.toast({ message: data, color: 'success', duration: 1500 });
            } catch (error) {
                console.error(error);
                this.toast({ message: 'Error deleting item', color: 'danger', duration: 1500 });
            } finally {
                this.isLoading = false

            }
        },
        async downloadData(projectId: string, fields: string[], applyFilters: boolean) {
            this.isTSVLoading = true
            const model = this.currentModel
            const downloadRequest = { format: "tsv", fields }
            try {
                const requestData = applyFilters ? { ...this.stores[model].searchForm, ...downloadRequest } : { ...downloadRequest }
                const { data } = await ItemService.getTsv(projectId, model, requestData)
                const href = URL.createObjectURL(data)
                const filename = `${model}_report.tsv`
                const link = document.createElement('a');
                link.href = href;
                link.setAttribute('download', filename); //or any other extension
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(href);
            } catch (e) {
                const axiosError = e as AxiosError
                this.toast({ message: axiosError.message, color: 'danger' })
            } finally {
                this.isTSVLoading = false
                this.showReport = false
            }
        },
        resetSearchForm() {
            const model = this.currentModel
            this.stores[model].searchForm = {}
        },
        resetPagination() {
            const model = this.currentModel
            this.stores[model].pagination.offset = 0
        },
    }
})
