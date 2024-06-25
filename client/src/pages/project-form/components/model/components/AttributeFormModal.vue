<template>
    <VaModal class="modal-crud" :model-value="!!attributeStore.attribute" @ok="submitAttribute"
        @cancel="resetAttribute()">
        <template #header>
            <h2 class="va-h2"> Editing filter</h2>
        </template>
        <VaForm ref="attributeForm">
            <p class="va-text-secondary">Fill in the fields</p>
            <VaDivider />
            <div v-if="attributeStore.attribute" class="row justify-space-between">
                <VaInput class="flex lg4 md4 sm12 xs12 mt-4" label="filter key (required)" :rules="[(v: string) => attributeStore.attributes.findIndex(it => it.key === v) === -1 || attributeStore.attributes.findIndex(it => it.key === v) === attributeStore.attributeId || 'Key must be unique',
    (v: string) => v.length > 0 || 'Key is required!']" placeholder="Type a value.."
                    v-model="attributeStore.attribute.key" />
                <VaInput class="flex lg4 md4 sm12 xs12 mt-4" placeholder="Type a value.." :rules="[(v: string) => attributeStore.attributes.findIndex(it => it.label === v) === -1 || attributeStore.attributes.findIndex(it => it.label === v) === attributeStore.attributeId || 'label must be unique',
    (v: string) => v.length > 0 || 'Label is required!']" v-model="attributeStore.attribute.label"
                    label="Attribute label (required)" />
                <VaInput class="flex lg8 md8 sm12 xs12 mt-4" v-model="attributeStore.attribute.description"
                    label="filter description (optional)" placeholder="Type a brief description of the project" />
                <VaSelect class="flex lg6 md6 sm12 xs12 mt-4" label="Is required?" v-model="attributeStore.attribute.required"
                    :options="[true, false]" />
                <div class="flex lg12 md12 sm12 xs12">
                    <VaSelect class="flex lg6 md12 sm6 xs12 mt-4 mb-2" label="filter type" v-model="fType"
                        :options="fieldTypes" />
                    <div class="row row-equal">
                        <div class="flex lg12 md12">
                            <VaCard square outlined>
                                <VaCardTitle>{{ fType }}</VaCardTitle>
                                <VaCardContent v-if="fType === 'input'">
                                    <VaSelect label="input type" v-model="input.input_type"
                                        :options="['text', 'number', 'date']" />
                                    <VaInput label="regex" v-model="input.regex" />
                                </VaCardContent>
                                <VaCardContent v-else-if="fType === 'select'">
                                    <VaSelect label="Is field multiple choice" v-model="select.multi"
                                        :options="[true, false]" />
                                    <div class="row justify-center">
                                        <div v-for="(choice, index) in select.choices" class="flex lg12 md12 sm12 xs12"
                                            :key="index">
                                            <VaInput :label="`Choice number: ${index}`" class="mt-2"
                                                :rules="[(v: string) => v.length > 0 || 'Insert a valid value', (v: string) => select.choices.findIndex(c => c === v) === -1 || select.choices.findIndex(c => c === v) === index || 'Value must be unique']"
                                                v-model="select.choices[index]">
                                                <template #appendInner>
                                                    <VaButton :disabled="index === 0 || index === 1" color="danger"
                                                        size="small" icon="delete"
                                                        @click="select.choices = [...select.choices.slice(0, index), ...select.choices.slice(index + 1)]" />
                                                </template>
                                            </VaInput>
                                        </div>
                                        <div class="flex">
                                            <VaButton class="mt-2" size="small" @click="select.choices.push('')"
                                                icon="add">
                                                New choice
                                            </VaButton>
                                        </div>
                                    </div>
                                </VaCardContent>
                                <VaCardContent v-else>
                                    <div class="row justify-space-between">
                                        <div class="flex lg4 md4 sm12 xs12">
                                            <VaCounter manual-input
                                                :rules="[(v: any) => numberRule(v) || 'Value must be a number', (v: number) => v < range.max || 'min must be greater than max']"
                                                type="number" label="min" v-model="range.min" />
                                        </div>
                                        <div class="flex lg4 md4 sm12 xs12">
                                            <VaCounter manual-input
                                                :rules="[(v: any) => numberRule(v) || 'Value must be a number', (v: number) => v > range.min || 'max must be greater than min']"
                                                type="number" label="max" v-model="range.max" />
                                        </div>
                                        <div class="flex lg8 md8 sm12 xs12">
                                            <VaInput :rules="[(v: string) => v.length > 0 || 'unit is mandatory']"
                                                v-model="range.unit" label="unit"></VaInput>
                                        </div>
                                    </div>
                                </VaCardContent>
                            </VaCard>
                        </div>
                    </div>
                </div>
            </div>
        </VaForm>
    </VaModal>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue';
import { Input, Select, Range, fieldTypes, Filter } from '../../../../../data/types'
import { useForm } from 'vuestic-ui'
import { useAttributeStore } from '../../../../../stores/attribute-store'

const { validate } = useForm('attributeForm')

const attributeStore = useAttributeStore()

const numberRule = (v: any) => typeof v === 'number' && !isNaN(v)

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

const fType = ref('input')

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

</script>
