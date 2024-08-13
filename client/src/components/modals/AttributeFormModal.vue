<template>
    <VaModal max-height="500px" fixed-layout :model-value="!!attributeStore.attribute" @ok="submitAttribute"
        @cancel="resetAttribute()">
        <template #header>
            <h2 class="va-h2"> Filter editing</h2>
        </template>
        <VaForm v-if="attributeStore.attribute" ref="attributeForm">
            <div class="row align-end">
                <div class="flex lg6 md6 sm12 xs12 p-6">
                    <VaInput label="filter key (required)" :rules="keyRules" placeholder="Type a value.."
                        v-model="attributeStore.attribute.key" />
                </div>
                <div class="flex lg6 md6 sm12 xs12 p-6">
                    <VaInput placeholder="Type a value.." :rules="labelRules" v-model="attributeStore.attribute.label"
                        label="Attribute label (required)" />
                </div>
                <div class="flex lg12 md12 sm12 xs12 p-6">
                    <VaInput v-model="attributeStore.attribute.description" label="filter description (optional)"
                        placeholder="Type a brief description of the filter" />
                </div>
                <div class="flex p-6">
                    <VaCheckbox v-model="attributeStore.attribute.required" label="Is mandatory?"
                        :messages="['Set this attribute as required']"></VaCheckbox>
                </div>
            </div>
            <VaTabs v-model="fType">
                <template #tabs>
                    <VaTab v-for="(tab, index) in ['input', 'select', 'range']" :name="tab" :key="index" :label="tab" />
                </template>
            </VaTabs>
            <VaCard square outlined>
                <VaCardContent class="row" v-if="fType === 'input'">
                    <VaSelect class="flex lg8 md8 sm12 xs12 p-6" label="input type" v-model="input.input_type"
                        :options="['text', 'number', 'date']" />
                    <VaInput class="flex lg8 md8 sm12 xs12 p-6" label="regex" v-model="input.regex" />
                </VaCardContent>
                <VaCardContent class="row" v-else-if="fType === 'select'">
                    <div class="flex lg12 md12 sm12 xs12 p-6">
                        <VaCheckbox v-model="select.multi" label="Is field multiple choice"
                            :messages="['It will be possible to select more the one option']"></VaCheckbox>
                    </div>
                    <div v-for="(choice, index) in select.choices" class="flex lg8 md8 sm12 xs12 p-6" :key="index">
                        <VaInput :label="`Choice number: ${index}`" class="mt-2" :rules="choiceRules(index)"
                            v-model="select.choices[index]">
                            <template #appendInner>
                                <VaButton :disabled="index === 0" color="danger" size="small" icon="delete"
                                    @click="sliceChoices(index)" />
                            </template>
                        </VaInput>
                    </div>
                    <div class="flex lg12 md12 sm12 xs12 p-6">
                        <VaButton size="small" @click="select.choices.push('')" icon="add">
                            New choice
                        </VaButton>
                    </div>
                </VaCardContent>
                <VaCardContent v-else>
                    <div class="row">
                        <div class="flex lg4 md4 sm12 xs12 p-6">
                            <VaCounter manual-input :rules="minRules" type="number" label="min" v-model="range.min" />
                        </div>
                        <div class="flex lg4 md4 sm12 xs12 p-6">
                            <VaCounter manual-input :rules="maxRules" type="number" label="max" v-model="range.max" />
                        </div>
                        <div class="flex lg8 md8 sm12 xs12 p-6">
                            <VaInput :rules="unitRules" v-model="range.unit" label="unit">
                            </VaInput>
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
        </VaForm>
    </VaModal>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue';
import { Input, Select, Range, Filter } from './../../data/types'
import { useForm } from 'vuestic-ui'
import { useAttributeStore } from './../../stores/attribute-store'

const { validate } = useForm('attributeForm')

const attributeStore = useAttributeStore()


const keyRules = [
    (v: string) => attributeStore.attributes.findIndex(it => it.key === v) === -1 || attributeStore.attributes.findIndex(it => it.key === v) === attributeStore.attributeId || 'Key must be unique',
    (v: string) => v.length > 0 || 'Key is required!',
]

const labelRules = [
    (v: string) => attributeStore.attributes.findIndex(it => it.label === v) === -1 || attributeStore.attributes.findIndex(it => it.label === v) === attributeStore.attributeId || 'Label must be unique',
    (v: string) => v.length > 0 || 'Label is required!',
]

const choiceRules = (index: number) => [
    (v: string) => v.length > 0 || 'Insert a valid value',
    (v: string) => select.value.choices.findIndex(c => c === v) === -1 || select.value.choices.findIndex(c => c === v) === index || 'Value must be unique',
]

const minRules = [
    (v: any) => typeof v === 'number' && !isNaN(v) || 'Value must be a number',
    (v: number) => v < range.value.max || 'Min must be less than Max',
]

const maxRules = [
    (v: any) => typeof v === 'number' && !isNaN(v) || 'Value must be a number',
    (v: number) => v > range.value.min || 'Max must be greater than Min',
]

const unitRules = [(v: string) => v.length > 0 || 'Unit is mandatory']



watch(() => attributeStore.attribute, (newValue) => {
    if (!newValue) return

    const filterKeys = Object.keys(newValue.filter)
    if (filterKeys.includes('input_type')) {
        input.value = { ...newValue.filter as Input }
        fType.value = 'input'
    }
    else if (filterKeys.includes('choices')) {
        const newSelect = newValue.filter as Select
        select.value = { ...newSelect }
        select.value.choices = [...newSelect.choices]
        fType.value = 'select'
    }
    else {
        range.value = { ...newValue.filter as Range }
        fType.value = 'range'
    }

})

const fType = ref<'input' | 'range' | 'select'>('input')

const initSelect: Select = {
    multi: false,
    choices: ['', '']
}
const select = ref<Select>({ ...initSelect })

const initInput: Input = {
    regex: "",
    input_type: "text"
}
const input = ref<Input>({ ...initInput })
const initRange: Range = {
    min: 0,
    max: 0,
    unit: ''
}
const range = ref<Range>({ ...initRange })

function resetForms() {
    input.value = { ...initInput }
    select.value = { ...initSelect }
    select.value.choices = [...['', '']]
    range.value = { ...initRange }
}

function submitAttribute() {
    const { attribute, attributeId } = attributeStore
    if (!validate()) return
    if (attribute) {
        if (fType.value === 'input') {
            attribute.filter = { ...input.value }
        } else if (fType.value === 'select') {
            attribute.filter = { ...select.value }
        } else {
            attribute.filter = { ...range.value }
        }
        if (attributeId !== null) {
            attributeStore.attributes = [
                ...attributeStore.attributes.slice(0, attributeId),
                { ...attribute },
                ...attributeStore.attributes.slice(attributeId + 1),
            ];
        } else {
            attributeStore.attributes.push({ ...attribute as Filter })
        }
        resetAttribute()
    }
}
function resetAttribute() {
    resetForms()
    attributeStore.reset()
}

function sliceChoices(index: number) {
    select.value.choices = [...select.value.choices.slice(0, index), ...select.value.choices.slice(index + 1)]
}

</script>
