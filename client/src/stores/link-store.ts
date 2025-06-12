import { defineStore } from 'pinia'
import AuthService from '../services/clients/AuthService'
import { FileModelLink, LinkType } from '../data/types'
import LinkService from '../services/clients/LinkService'
import { catchError, success } from '../composables/toastMessages'

const staticFilters: Record<string, any> = {
    sort_order: null,
    sort_column: null,
}
const initPagination = {
    offset: 0,
    limit: 10,
}

export const useLinkStore = defineStore('link', {
    state: () => {
        return {
            showLinkForm: false,
            linkType: 'protocols' as LinkType,
            isTableLoading: false,
            files: [] as { file: File; name: string; description: string, type: LinkType, preview: File }[],
            sort: { ...staticFilters },
            filter: "",
            pagination: { ...initPagination },
            links: [] as FileModelLink[],
            total: 0,
        }
    },
    actions: {
        resetForm() {
            this.files = []
        },
        toggleModal() {
            this.showLinkForm = !this.showLinkForm
        },
        resetFilters() {
            this.filter = ""
            this.resetPagination()
            this.sort = { ...staticFilters }
        },
        async fetchProjectModelLinks(projectId: string, modelName: string, type: LinkType) {
            const params = { filter: this.filter, ...this.pagination, ...this.sort, type }
            try {
                this.isTableLoading = true
                const { data } = await LinkService.getProjectModelLinks(projectId, modelName, params);
                this.links = [...data.data];
                this.total = data.total;
            } catch (e) {
                catchError(e)
            } finally {
                this.isTableLoading = false
            }
        },
        async deleteLink(projectId: string, modelName: string, name: string, type: LinkType) {
            try {
                const { data } = await LinkService.deleteLink(projectId, modelName, name, type);
                success(data, 1500)
            } catch (error) {
                catchError(error)
            }
        },
        async downloadFile(hash: string, filename: string) {
            try {
                const { data } = await LinkService.downloadLinks(hash)

                const href = URL.createObjectURL(data)
                const link = document.createElement('a');
                link.href = href;
                link.setAttribute('download', filename); //or any other extension
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(href);
            } catch (e) {
                catchError(e)
            }
        },
        async downloadFiles(projectId: string, modelName: string, type: LinkType) {
            try {
                const { data } = await LinkService.downloadFiles(projectId, modelName, type)
                const href = URL.createObjectURL(data)
                const link = document.createElement('a');
                link.href = href;
                link.setAttribute('download', `${projectId}_${modelName}_${type}_files.zip`);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(href);
            } catch (e) {
                catchError(e)
            }
        },
        resetPagination() {
            this.pagination = { ...initPagination }
        },
    }
})
