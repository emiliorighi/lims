<template>
    <div class="row">
        <va-card class="flex lg12 md12 sm12 xs12">
            <va-card-title>
                Project creation
            </va-card-title>
            <va-card-content>
                <va-form ref="schemaForm">
                    <va-stepper linear v-model="currentStep" :steps="steps">
                        <template #step-content-0>
                            <va-input :rules="[(v:string) => v.length > 3 || 'name is mandatory, at least 3 characters']"
                                class="mt-4" label="name" v-model="schema.name" />
                            <va-input class="mt-4" label="version" v-model="schema.version"
                                :rules="[(v:string) => v.length > 0 || 'version is mandatory']" />
                            <va-input class="mt-4" label="Project description" v-model="schema.description" />
                        </template>
                        <template #step-content-1>
                            <div class="row align-center">
                                <div v-for="(attr, index) in sampleAttributes" :key="index" class="flex lg5 md5 sm10 xs10">
                                    <va-card>
                                        <va-card-actions align="right">
                                            <va-button size="small" icon="done"/>
                                            <va-button size="small" color="danger" icon="delete"
                                                @click="sampleAttributes.splice(index, 1)">Delete Field</va-button>
                                        </va-card-actions>
                                        <va-divider />
                                        <va-card-content>
                                            <va-input class="mb-4" label="key" v-model="attr.key" :rules="[(v:string) => sampleAttributes.filter((m) => m.key === v).length > 0 || `${v} already exists`,
                                            (v:string) => v.length > 0 || 'key is mandatory']" />
                                            <va-input :rules="[(v:string) => v.length > 0 || 'label is mandatory']"
                                                class=" mb-4" label="label" v-model="attr.label" />
                                            <va-input class="mb-4" label="description" v-model="attr.description" />
                                            <va-checkbox v-model="attr.required" class="mt-4" label="Attribute is required" />
                                            <FieldTypeForm @on-field-submit="(value) => attr.filter = { ...value }" />
                                        </va-card-content>
                                    </va-card>
                                </div>
                                <div class="flex">
                                    <va-button icon="add" size="large" @click="sampleAttributes.push({ ...initFilter })" />
                                </div>
                            </div>
                        </template>
                        <template #step-content-2>
                            <va-select class="mt-4" v-model="sampleIdentifiers" multiple
                                :options="schema.sample.fields.map(f => f.key)" label="ID fields"
                                :messages="['Add a list of fields that will be formatted as t']"
                                :error="!sampleIdentifiers.length || matchedSampleIds.length !== sampleIdentifiers.length" />
                        </template>
                    </va-stepper>
                </va-form>
            </va-card-content>
        </va-card>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { Filter } from '../../data/types';
import FieldTypeForm from './components/FieldTypeForm.vue'
import { defineVaStepperSteps, useForm } from 'vuestic-ui'
import { useSchemaStore } from '../../stores/schemas-store'

const sampleIdentifiers = ref([])
const matchedSampleIds = computed(() => {
    return sampleIdentifiers.value.filter(id => schema.sample.fields.map(f => f.key).includes(id))
})
const experimentIdentifiers = ref([])
const matchedExperimentIds = computed(() => {
    return sampleIdentifiers.value.filter(id => schema.sample.fields.map(f => f.key).includes(id))
})
const { validate } = useForm('schemaForm')

const { schema } = useSchemaStore()
const currentStep = ref(0)
const steps = ref(defineVaStepperSteps([
    {
        label: 'Project Information', beforeLeave: (step) => { step.hasError = !validate() }
    },
    {
        label: 'Sample Fields', beforeLeave: (step) => { step.hasError = !validate() }
    },
    {
        label: 'Sample id fields', beforeLeave: (step) => { step.hasError = !validate() }
    }
    // {
    //     label: 'Experiment', beforeLeave: (step) => {
    //         step.hasError = model.value.b === ''
    //         return !step.hasError
    //     },
    //     icon: 'flask'
    // },
]))
const initFilter: Filter = {
    label: '',
    description: '',
    key: '',
    required: false,
    filter: {
        input_type: "text",
    }
}

const format = ref('json')
const url = ref('')
const mode = ref('form')
// const schema = ref<{
//     name: string,
//     version: string,
//     description?: string,
//     sample: Record<string, any>[],
//     experiment: Record<string, any>[]
// }>({
//     name: '',
//     version: '',
//     sample: [],
//     experiment: []
// })
const sampleAttributes = ref<Filter[]>([])
const experimentAttributes = ref<Filter[]>([])

const id = computed(() => {
    if (schema.name && schema.version) {
        schema.id = `${schema.name}_${schema.version}`
    }
    return schema.id
})
</script>