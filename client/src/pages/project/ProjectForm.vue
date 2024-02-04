<template>
    <div class="row">
        <div class="flex">
            <va-button>draft</va-button>
        </div>
        <div class="flex">
            <va-button>validate</va-button>
        </div>
        <div class="flex">
            <va-button>reset</va-button>
        </div>
    </div>
    <div class="row">
        <div class="flex">
            <va-card>
                <va-card-title>
                    Project upload
                </va-card-title>
                <va-form>
                    <va-divider />
                    <va-card-content>
                        <va-chip @click="mode = 'form'">Form</va-chip>
                        <va-chip @click="mode = 'url'">URL</va-chip>
                    </va-card-content>
                    <va-card-content v-if="mode === 'form'">
                        <va-input v-model="schema.name">

                        </va-input>
                        <va-input v-model="schema.version">

                        </va-input>
                        <va-input v-model="schema.description">

                        </va-input>
                        <va-collapse stateful header="SAMPLE ATTRIBUTES">
                            
                        </va-collapse>
                    </va-card-content>
                    <va-card-content else>
                        <va-radio v-model="format" option="json"></va-radio>
                        <va-radio v-model="format" option="yaml"></va-radio>
                        <va-input v-model="url">
                        </va-input>
                    </va-card-content>
                </va-form>
            </va-card>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';



const format = ref('json')
const url = ref('')
const mode = ref('form')
const schema = ref<{
    name: string,
    version: string,
    description?: string,
    sample: Record<string, any>[],
    experiment: Record<string, any>[]
}>({
    name: '',
    version: '',
    sample: [],
    experiment: []
})
const schemaId = computed(()=>{
    return `${schema.value.name}_${schema.value.version}`
})
</script>