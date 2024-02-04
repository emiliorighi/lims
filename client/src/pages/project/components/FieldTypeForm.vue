<template>
    <div class="row">
        {{ validField }}
        <div class="flex lg12 md12 sm12 xs12">
            <va-chip v-for="f in ['input', 'select', 'range']" @click="fieldSelection = f">{{ f }}</va-chip>
            <!-- <va-button color="danger">reset</va-button> -->
        </div>
        <div v-if="fieldSelection === 'input'" class="flex sm12 xs12">
            <va-select label="input type" v-model="input.input_type" :options="['text', 'number', 'date']"></va-select>
            <va-input label="regex" v-model="input.regex" />
        </div>
        <div v-else-if="fieldSelection === 'select'" class="flex sm12 xs12">
            <va-checkbox v-model="select.multi" label="Multiple choice"></va-checkbox>
            <div v-for="(c, index) in select.choices">
                <va-input :rules="[(v: string) => v.length > 0 || 'value is mandatory']"
                    v-model="select.choices[index]"></va-input>
                <va-button color="danger" icon="delete" @click="select.choices.splice(index, 1)"></va-button>
            </div>
            <va-button icon="add" @click="select.choices.push(' ')">Add new value</va-button>
        </div>
        <div v-else class="flex sm12 xs12">
            <va-input :rules="[(v: number) => v >= range.max || 'min must be greater than max']" type="number" label="min"
                v-model="range.min"></va-input>
            <va-input :rules="[(v: number) => v <= range.min || 'min must be greater than max']" type="number" label="max"
                v-model="range.max"></va-input>
            <va-input :rules="[(v: string) => v.length > 0 || 'unit is mandatory']" v-model="range.unit"
                label="unit"></va-input>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { Select, Input, Range } from '../../../data/types'

const fieldSelection = ref('input')
const emits = defineEmits(['onFieldSubmit'])
const validField = computed(() => {
    if (fieldSelection.value === 'input') {
        const { input_type } = input.value
        return input_type.length > 0
    } else if (fieldSelection.value === 'select') {
        const { choices } = select.value
        return choices.length > 0
    } else {
        const { min, max, unit } = range.value
        return min > max && unit.length > 0
    }
})
// watch((valid)=>{

// })
const choices = ref([' '])
const select = ref<Select>({
    multi: false,
    choices: []
})
const input = ref<Input>({
    regex: "",
    input_type: "text"
})
const range = ref<Range>({
    min: 0,
    max: 0,
    unit: ''
})



</script>