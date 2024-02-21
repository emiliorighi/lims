import { defineStore } from 'pinia'
import { Filter } from '../data/types'

const defaultItem: Filter = {
    key: '',
    label: '',
    description: '',
    filter: {
        input_type: 'text',
        regex: ''
    },
    required: false
};

export const useAttributeStore = defineStore('attribute', {
    state: () => {
        return {
            attribute: null as Filter | null,
            attributeId: null as number | null,
            attributes: [] as Filter[]
        }
    },
    actions: {
        reset() {
            this.attribute = null
            this.attributeId = null
        },
        initAttribute(){
            this.attribute = {...defaultItem}
        }

    }
})
