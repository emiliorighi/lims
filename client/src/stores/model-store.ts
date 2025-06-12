import { defineStore } from 'pinia'
import {  ResearchModel, ResearchFilter } from '../data/types'
import StatsService from '../services/clients/StatsService'

export const useModelStore = defineStore('model', {
    state: () => {
        return {
            currentModel: null as ResearchModel | null,
            showDeleteConfirmation: false,
            filters: [] as ResearchFilter[],
            refModel: null as ResearchModel | null,
            idFormat: [] as string[],
            isUpdate: false,
            records: 0,
            protocols: 0,
            images: 0,
        }
    },
    actions: {
        async getStats(projectId: string, modelName: string) {
            const { data } = await StatsService.getModelStats(projectId, modelName)
            this.records = data.records
            this.protocols = data.protocols
            this.images = data.images
        },
        setModel(models: ResearchModel[], modelName: string) {
            const matchedModel = models.find(({ name }) => name === modelName)
            if (matchedModel) {
                this.currentModel = { ...matchedModel }
                this.filters = [...this.currentModel.fields]
                this.idFormat = [...this.currentModel.id_format]
            }
            this.refModel = models.find(({ name }) => name === this.currentModel?.reference_model) ?? null
        },
    }
})
