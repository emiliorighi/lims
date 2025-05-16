import { defineStore } from 'pinia'
import { useToast } from 'vuestic-ui/web-components'
import { AxiosError } from 'axios'
import AuthService from '../services/clients/AuthService'
import RecordService from '../services/clients/RecordService'
import { ErrorResponseData, ResearchRecord } from '../data/types'
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
            showTSVImportModal: false,
            idToDelete: null as null | string,
            relatedRecordCount: 0,
            tableLoading: false,
            refRecords: [] as string[],
            recordStats: [] as [string, number][],
            isTSVLoading: false,
            isRefRecord: false,
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
            const mappedEntries = Object.entries(this.searchForm).map(([key, query]) => {
                //generate query key operator
                return Object.entries(query).map(([op, value]) => [`${key}__${op}`, value])
            }).flat()
            return Object.fromEntries(mappedEntries)
        },
        toggleRecordForm() {
            this.showRecordForm = !this.showRecordForm
        },
        resetForm() {
            this.recordForm = {}
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
        async fetchRefRecords(projectId: string, modelName: string) {
            try {
                const { data } = await StatsService.getStats(projectId, modelName, 'reference_id', {})
                this.refRecords = Object.keys(data)
            } catch (err) {
                this.catchError(err)
            }
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
        toggleChartModal() {
            this.showChartModal = !this.showChartModal
        },
        toggleImportModal() {
            this.showTSVImportModal = !this.showTSVImportModal
        },
        toggleDeleteModal() {
            this.showDeleteConfirmation = !this.showDeleteConfirmation
        },
        toggleReportModal() {
            this.showReportModal = !this.showReportModal
        },
        async getRecordStats(field: string, query: Record<string, any>) {
            try {
                const { data } = await StatsService.getRecordStats(field, query)
                this.recordStats = Object.entries(data)
            } catch (error) {
                this.catchError(error)
            }
        },
        async downloadData(projectId: string, modelName: string, fields: string[], applyFilters: boolean) {
            const downloadRequest = { format: "tsv", fields: fields.join(',') }
            try {
                this.isTSVLoading = true
                const requestData = applyFilters ? { ...this.buildQuery(), ...downloadRequest } : { ...downloadRequest }
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
        async triggerDelete(projectId: string, modelName: string, item: ResearchRecord) {
            this.idToDelete = item.item_id
            await this.fetchRelatedRecords(projectId, modelName, item.item_id, {})
            this.showDeleteConfirmation = true
        },
        viewRecord(item: ResearchRecord) {
            this.isRefRecord = false
            this.record = { ...item }
            this.showRecordDetails = !this.showRecordDetails
        },
        async viewRelatedRecord(projectId: string, refModelName: string | undefined, id: string | undefined) {
            if (!id || !refModelName) return
            await this.fetchItem(projectId, refModelName, id)
            this.isRefRecord = true
            this.showRecordDetails = true
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
