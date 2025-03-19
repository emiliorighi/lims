import { defineStore } from 'pinia'
import { useToast } from 'vuestic-ui/web-components'
import { AxiosError } from 'axios'
import AuthService from '../services/clients/AuthService'
import RecordService from '../services/clients/RecordService'
import { ResearchFilter, ResearchRecord } from '../data/types'

const staticFilters: Record<string, any> = {
    sort_order: null,
    sort_column: null,
}
const initPagination = {
    offset: 0,
    limit: 10,
}

export const useRecordStore = defineStore('record', {
    state: () => {
        return {
            showRecordForm: false,
            showReportModal: false,
            showChartModal: false,
            tableLoading: false,
            isTSVLoading: false,
            idToUpdate: null as null | string,
            recordForm: {} as Record<string, any>,
            sort: { ...staticFilters },
            pagination: { ...initPagination },
            searchForm: {} as Record<string, any>,
            records: [] as ResearchRecord[],
            total: 0,
            record: null as null | Record<string, any>,
            showItemDetails: false,
            toast: useToast().init,
        }
    },
    actions: {
        async fetchRecords(projectId: string, modelName: string) {
            const params = { ...this.searchForm, ...this.pagination, ...this.sort }
            try {
                this.tableLoading = true
                const { data } = await RecordService.getItems(projectId, modelName, params);
                this.records = [...data.data];
                this.total = data.total;
            } catch (e) {
                this.toast({ message: 'Error fetching data', color: 'danger' })
            } finally {
                this.tableLoading = false
            }
        },
        initForm(fields: ResearchFilter[]) {
            const entries = fields.map(({ key, type, multi }) => {
                let value = "" as any
                if (type === 'select' && multi) value = []
                return [key, value]
            })
            this.recordForm = { ...Object.fromEntries(entries) }
        },
        setForm(id: string, recordData: Record<string, any>) {
            this.idToUpdate = id
            this.recordForm = { ...recordData }
        },
        resetForm() {
            this.recordForm = {}
            this.idToUpdate = null
        },
        async fetchItem(projectId: string, modelName: string, itemId: string) {
            try {
                const { data } = await RecordService.getItem(projectId, itemId, modelName)
                this.record = { ...data }
            } catch (e) {
                let message: string
                const axiosError = e as AxiosError

                if (axiosError.response?.data) {
                    message = (axiosError.response.data as { message: string }).message || axiosError.response.data as string
                } else {
                    message = axiosError.message
                }
                this.toast({ message: message, color: 'danger' })
            }
        },
        async deleteItem(projectId: string, modelName: string, idToDelete: string) {
            try {
                const { data } = await AuthService.deleteItem(projectId, idToDelete, modelName);
                this.toast({ message: data, color: 'success', duration: 1500 });
            } catch (error) {
                console.error(error);
                this.toast({ message: 'Error deleting item', color: 'danger', duration: 1500 });
            }
        },
        async downloadData(projectId: string, modelName: string, fields: string[], applyFilters: boolean) {
            const downloadRequest = { format: "tsv", fields }
            try {
                this.isTSVLoading = true
                const requestData = applyFilters ? { ...this.searchForm, ...downloadRequest } : { ...downloadRequest }
                const { data } = await RecordService.getTsv(projectId, modelName, requestData)
                const href = URL.createObjectURL(data)
                const filename = `${modelName}_report.tsv`
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
                this.showReportModal = false
            }
        },
        resetSearchForm() {
            this.searchForm = {}
        },
        resetPagination() {
            this.pagination = { ...initPagination }
        },
    }
})
