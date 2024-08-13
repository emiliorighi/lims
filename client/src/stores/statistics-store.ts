import { defineStore } from 'pinia'
import { VaChartItem } from '../data/types'


export const useStatisticsStore = defineStore('statistics', {
    state: () => {
        return {
            charts: [] as VaChartItem[]
        }
    },

    actions: {

    },
})
