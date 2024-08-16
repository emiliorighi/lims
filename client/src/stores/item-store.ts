import { defineStore } from 'pinia'
import { ItemModel, ModelSearchForm, ModelType } from '../data/types'
import ItemService from '../services/clients/ItemService'
import { useToast } from 'vuestic-ui/web-components'
import { AxiosError } from 'axios'

function parseQuery(pagination: Record<string, any>, searchForm: Record<string, any>) {
    let q = { ...pagination }
    const { query, ...fields } = searchForm
    const validFilters = Object.fromEntries(Object.entries(query).filter(([k, v]) => v))
    if (Object.keys(validFilters).length) {
        q = { ...q, ...validFilters }
    }
    if (Object.entries(fields).filter(([k, v]) => v).length) {
        q = { ...q, ...fields }
    }
    return q
}

function triggerDownload(data: Blob | MediaSource, model: ModelType) {
    const href = URL.createObjectURL(data)
    const filename = `${model}_report.tsv`
    const link = document.createElement('a');
    link.href = href;
    link.setAttribute('download', filename); //or any other extension
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(href);
}

const initSearchForm: ModelSearchForm = {
    filter: '',
    query: {},
    sort_column: '',
    sort_order: 'asc'
}

const initPagination = {
    offset: 0,
    limit: 10,
}

export const useItemStore = defineStore('item', {
    state: () => {
        return {
            item: undefined as ItemModel | undefined,
            items: [] as ItemModel[],
            showForm: false,
            showReport: false,
            isLoading: false,
            searchForm: { ...initSearchForm },
            showItemDetails: false,
            showDeleteConfirm: false,
            idToDelete: undefined as undefined | string,
            pagination: { ...initPagination },
            toast: useToast().init,
            total: 0
        }
    },

    actions: {

        async fetchItems(projectId: string, model: ModelType) {
            this.isLoading = true
            const query = parseQuery(this.pagination, this.searchForm)
            try {
                const { data } = await ItemService.getItems(projectId, model, query);
                this.items = [...data.data];
                this.total = data.total;
            } catch (e) {
                this.toast({ message: 'Error fetching data', color: 'danger' })
            } finally {
                this.isLoading = false
            }

        },
        async fetchItem(projectId: string, itemId: string, m: ModelType) {
            this.isLoading = true
            try {
                const { data } = await ItemService.getItem(projectId, itemId, m)
                this.item = { ...data }
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

        async deleteItem(projectId: string, model: ModelType) {
            if (!this.idToDelete) return
            this.isLoading = true

            try {
                const { data } = await ItemService.deleteItem(projectId, this.idToDelete, model);
                this.toast({ message: data, color: 'success', duration: 1500 });
                // reset();
            } catch (error) {
                console.error(error);
                this.toast({ message: 'Error deleting item', color: 'danger', duration: 1500 });
            } finally {
                this.isLoading = false

            }
        },
        async downloadData(requestData: Record<string, any>, projectId: string, model: ModelType) {
            this.isLoading = true
            try {

                const response = await ItemService.getTsv(projectId, model, requestData)
                const data = response.data
                triggerDownload(data, model)
            } catch (e) {
                const axiosError = e as AxiosError
                this.toast({ message: axiosError.message, color: 'danger' })
            } finally {
                this.isLoading = false
                this.showReport = false
            }
        },

        resetSearchForm() {
            this.searchForm = { ...initSearchForm }
        },
        resetPagination() {
            this.pagination = { ...initPagination }
        },
    }
})
