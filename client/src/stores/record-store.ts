import { defineStore } from 'pinia'
import { useToast } from 'vuestic-ui/web-components'
import { AxiosError } from 'axios'
import AuthService from '../services/clients/AuthService'
import RecordService from '../services/clients/RecordService'
import { ErrorResponseData, ResearchFilter, ResearchRecord } from '../data/types'
import StatsService from '../services/clients/StatsService'

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
            showRecordDetails: false,
            showChartModal: false,
            showDeleteConfirmation: false,
            showFilters: false,
            idToDelete: null as null | string,
            relatedRecordCount: 0,
            tableLoading: false,
            isTSVLoading: false,
            idToUpdate: null as null | string,
            recordForm: {} as Record<string, any>,
            sort: { ...staticFilters },
            pagination: { ...initPagination },
            searchForm: {} as Record<string, any>,
            records: [] as ResearchRecord[],
            total: 0,
            record: null as null | ResearchRecord,
            toast: useToast().init,
        }
    },
    actions: {

        buildQuery() {
            if (this.searchForm) {
                const searchFormEntries = Object.values(this.searchForm).map(value => Object.entries(value)).flat()
                return Object.fromEntries(searchFormEntries);
            } else {
                return {}
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
        async fetchRecords(projectId: string, modelName: string) {
            const params = { ...this.buildQuery(), ...this.pagination, ...this.sort }
            try {
                this.tableLoading = true
                const { data } = await RecordService.getItems(projectId, modelName, params);
                this.records = [...data.data];
                this.total = data.total;
            } catch (e) {
                this.catchError(e)
            } finally {
                this.tableLoading = false
            }
        },
        async fetchRelatedRecords(projectId: string, modelName: string, itemId: string, query: Record<string, any>) {
            const { data } = await RecordService.getRelatedRecords(projectId, modelName, itemId, query)
            this.relatedRecordCount = data.total
        },
        async getFieldFrequencies(projectId: string, modelName: string, field: string, ignoreQuery?: boolean) {
            try {
                const { data } = await StatsService.getStats(projectId, modelName, field, ignoreQuery ? {} : this.buildQuery())
                return data
            } catch (err) {
                this.catchError(err)
            }
        },
        async fetchItem(projectId: string, modelName: string, itemId: string) {
            try {
                const { data } = await RecordService.getItem(projectId, itemId, modelName)
                this.record = { ...data }
            } catch (e) {
                this.catchError(e)
            }
        },
        async deleteItem(projectId: string, modelName: string, idToDelete: string) {
            try {
                const { data } = await AuthService.deleteItem(projectId, idToDelete, modelName);
                this.toast({ message: data, color: 'success', duration: 1500 });
            } catch (error) {
                this.catchError(error)
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
                this.catchError(e)
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
        catchError(error: any) {
            console.error(error)
            const axiosError = error as AxiosError<ErrorResponseData>
            let message
            if (axiosError.response && axiosError.response.data && axiosError.response.data.message) {
                message = axiosError.response.data.message

            } else {
                message = axiosError.message
            }
            this.toast({ message: message, color: 'danger' })
        },
    }
})
