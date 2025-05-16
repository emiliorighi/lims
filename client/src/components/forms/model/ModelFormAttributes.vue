<template>
    <div class="row">
        <div class="flex">
            <h2 class="va-h2">
                Attributes
            </h2>
            <p>Attributes can be considered as the columns of a tsv or spreasheet.</p>
        </div>
    </div>
    <ModelAttributes 
        v-model:model-attributes="modelData.fields" 
        :is-controlled-mode="isControlledMode"
        :has-records="hasRecords"
    />
    <ModelIdentifier 
        :model-name="modelData.name" 
        v-if="attributes.length"
        :refModelIdFields="selectedRefModel?.id_format" 
        :ref-model="modelData.reference_model"
        :attributes="attributes" 
        :disabled="isControlledMode"
        @change="(v) => modelData.id_format = v"
        :model-id="modelData.id_format" 
    />
    <VaInput style="visibility: hidden;" :rules="[(v: any) => attributes.length > 0 || 'Error']">
    </VaInput>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ResearchModel, EditMode } from '../../../data/types'
import ModelAttributes from '../ModelAttributes.vue'
import ModelIdentifier from '../ModelIdentifier.vue'

const props = defineProps<{
    modelValue: ResearchModel
    existingModels: ResearchModel[]
    mode: EditMode | 'create' | 'clone'
    hasRecords: boolean
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: ResearchModel): void
}>()

const modelData = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const isControlledMode = computed(() => props.mode === 'edit-controlled')
const attributes = computed(() => modelData.value.fields.map(({ key }) => key))
const selectedRefModel = computed(() => props.existingModels.find(m => m.name === modelData.value.reference_model))
</script> 