<template>
    <VaModal class="modal-crud" :model-value="!!attributeStore.attribute" @ok="submitAttribute" @cancel="resetAttribute()">
        <template #header>
            <h2 class="va-h2"> Editing attribute</h2>
        </template>
        <VaForm ref="attributeForm">
            <div v-if="attributeStore.attribute" class="row">
                <div class="flex sm12 xs12">
                    <VaInput label="Attribute key" :rules="[(v: string) => attributeStore.attributes.findIndex(it => it.key === v) === -1 || attributeStore.attributes.findIndex(it => it.key === v) === attributeStore.attributeId || 'Key must be unique',
                    (v: string) => v.length > 0 || 'Key is required!']" v-model="attributeStore.attribute.key" />
                </div>
                <div class="flex sm12 xs12">
                    <VaInput class="mt-2" :rules="[(v: string) => attributeStore.attributes.findIndex(it => it.label === v) === -1 || attributeStore.attributes.findIndex(it => it.label === v) === attributeStore.attributeId || 'label must be unique',
                    (v: string) => v.length > 0 || 'Label is required!']" v-model="attributeStore.attribute.label"
                        label="Attribute label" />
                </div>
                <div class="flex sm12 xs12">
                    <VaInput class="mt-2" v-model="attributeStore.attribute.description" label="Attribute description" />
                </div>
                <div class="flex sm12 xs12">
                    <VaSelect class="mt-2" label="Is the attribute required?" v-model="attributeStore.attribute.required"
                        :options="[true, false]" />
                </div>
                <div class="flex sm12 xs12">
                    <VaSelect class="mt-2" label="Attribute type" v-model="fType" :options="fieldTypes" />
                    <div class="row row-equal mt-2">
                        <div class="flex lg12 md12">
                            <VaCard square outlined>
                                <VaCardContent v-if="fType === 'input'">
                                    <VaSelect class="mt-2" label="input type" v-model="input.input_type"
                                        :options="['text', 'number', 'date']" />
                                    <VaInput label="regex" v-model="input.regex" />
                                </VaCardContent>
                                <VaCardContent v-else-if="fType === 'select'">
                                    <VaSelect class="mt-2" label="Is field multiple choice" v-model="select.multi"
                                        :options="[true, false]" />
                                    <div class="row justify-center">
                                        <div v-for="(choice, index) in select.choices" class="flex lg12 md12 sm12 xs12"
                                            :key="index">
                                            <VaInput :label="`Choice number: ${index}`" class="mt-2"
                                                :rules="[(v: string) => v.length > 0 || 'Insert a valid value', (v: string) => select.choices.findIndex(c => c === v) === -1 || select.choices.findIndex(c => c === v) === index || 'Value must be unique']"
                                                v-model="select.choices[index]">
                                                <template #appendInner>
                                                    <VaButton :round="false" :disabled="index === 0 || index === 1"
                                                        color="danger" size="small" icon="delete"
                                                        @click="select.choices = [...select.choices.slice(0, index), ...select.choices.slice(index + 1)]" />
                                                </template>
                                            </VaInput>
                                        </div>
                                        <div class="flex">
                                            <VaButton class="mt-2" size="small" @click="select.choices.push('')" icon="add">
                                                New choice
                                            </VaButton>
                                        </div>
                                    </div>
                                </VaCardContent>
                                <VaCardContent v-else>
                                    <VaCounter class="mt-2" manual-input
                                        :rules="[(v: any) => numberRule(v) || 'Value must be a number', (v: number) => v < range.max || 'min must be greater than max']"
                                        type="number" label="min" v-model="range.min" />
                                    <VaCounter class="mt-2" manual-input
                                        :rules="[(v: any) => numberRule(v) || 'Value must be a number', (v: number) => v > range.min || 'max must be greater than min']"
                                        type="number" label="max" v-model="range.max" />
                                    <VaInput class="mt-2" :rules="[(v: string) => v.length > 0 || 'unit is mandatory']"
                                        v-model="range.unit" label="unit"></VaInput>
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
import { computed, ref, watch } from 'vue';
import { Input, Select, Range, fieldTypes, Filter } from '../../../data/types'
import { useProjectStore } from '../../../stores/project-store';
import { useForm } from 'vuestic-ui'
import { useAttributeStore } from '../../../stores/attribute-store'

const { validate } = useForm('attributeForm')

const attributeStore = useAttributeStore()
const { project } = useProjectStore()

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
<style lang="scss" scoped>
.modal-crud {
    .VaInput {
        display: block;
    }

    .va-input-wrapper {
        display: block;
    }
}
</style>