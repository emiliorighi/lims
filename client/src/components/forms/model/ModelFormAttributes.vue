<template>
    <ModelAttributes 
        v-model:model-attributes="modelData.fields" 
        :is-controlled-mode="isControlledMode"
    />
    <VaInput style="visibility: hidden;" :rules="[(v: any) => attributes.length > 0 || 'Error']">
    </VaInput>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ResearchModel, EditMode } from '../../../data/types'
import ModelAttributes from '../ModelAttributes.vue'

const props = defineProps<{
    modelValue: ResearchModel
    mode: EditMode | 'create' | 'clone'
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: ResearchModel): void
}>()

const modelData = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const isControlledMode = computed(() => props.mode === 'edit-controlled')
const attributes = computed(() => modelData.value.fields.map(({ key }) => key).filter(Boolean))

</script> 