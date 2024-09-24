<template>
    <VaSelect clearable :label="label" v-model="selectedField" :multiple="multi" :options="options">
    </VaSelect>
</template>
<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    multi: boolean,
    options: string[]
    label: string
    value?: any
}>()

const selectedField = computed({
    get() {
        return props.value ? props.value : ''
    },
    set(v: any) {
        emits('valueChange', v)
    }
})

const emits = defineEmits(['valueChange'])
</script>