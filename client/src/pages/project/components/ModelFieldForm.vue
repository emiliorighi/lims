<template>
    <div>
        <va-collapse stateful :header="`${model} attributes`">
            <div v-for="(attr, index) in attributes" :key="index" class="row align-center justify-between">
                <div class="flex lg8 md8 sm8 xs8">
                    <va-input label="key" v-model="attr.key"
                        :error="attributes.filter((m) => m.key === attr.key).length > 1"
                        :error-messages="[`Attribute name ${attr.key} is already present`]">

                    </va-input>
                    <va-input label="label" v-model="attr.label">

                    </va-input>
                    <va-input label="description" type="textarea" v-model="attr.description">

                    </va-input>
                    <va-switch label="required" v-model="attr.required"></va-switch>
                    <va-divider>Attribute Type</va-divider>
                    <FieldTypeForm @on-field-submit="(value) => attr.filter = { ...value }" />

                </div>
                <div class="flex">
                    <va-button icon="delete" color="danger" @click="attributes.splice(index, 1)">
                        Delete Field
                    </va-button>
                </div>
            </div>
            <va-button class="mt-3" icon="add" @click="attributes.push({ ...initFilter })">Add
                new
                attribute</va-button>
        </va-collapse>
        
    </div>
</template>
<script setup lang="ts">
import FieldTypeForm from './FieldTypeForm.vue'
import { Filter } from '../../../data/types';
import { ref } from 'vue';

const props = defineProps<{
    model: 'sample' | 'experiment'
}>()

const initFilter: Filter = {
    label: '',
    description: '',
    key: '',
    required: false,
    filter: {
        input_type: "text",
    }
}
const attributes = ref<Filter[]>([])
</script>