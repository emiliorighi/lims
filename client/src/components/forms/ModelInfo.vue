<template>
    <div class="row justify-space-between align-end">
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput v-model="computedType"
                :rules="[(v: string) => v.length >= 3 || 'name is mandatory, at least 3 characters']"
                label="Model Name (required)" placeholder="Type here your model name (example: Sample)"
                :messages="['The name of your model (like sample, experiment etc.)']">
            </VaInput>
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <VaInput v-model="computedDescription" label="Model Description (optional)"
                placeholder="Type a description for your model">
            </VaInput>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';


const props = defineProps<{
    type: string
    description: string
}>()

const emits = defineEmits(['updateType', 'updateDescription'])

const computedType = computed({
    get() {
        return props.type
    },
    set(v: string) {
        emits('updateType', v)
    }
})

const computedDescription = computed({
    get() {
        return props.description
    },
    set(v: string) {
        emits('updateDescription', v)
    }
})

</script>