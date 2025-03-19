import { defineStore } from 'pinia'
import { Filter, ReseachModel, ResearchFilter } from '../data/types'

const modelForm: ReseachModel = {
    name: '',
    description: '',
    protocols: [],
    links: [],
    fields: [],
    id_format: []
}

export const useModelStore = defineStore('model', {
    state: () => {
        return {
            model: null as ReseachModel | null,
            modelForm: {...modelForm},
            records: [] as Record<string, any>[],
            protocols: [] as Record<string, any>[],
            filters: [] as ResearchFilter[],
        }
    },
    actions: {
        resetModelForm() {
            this.modelForm = {...modelForm}
        },
        async fetchRecords(params: Record<string, any>) {
            try {

            } catch (error) {

            } finally {

            }
        }

    }
})
