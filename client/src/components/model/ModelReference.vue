<template>
    <div class="row">
        <div class="flex">
            <h2 class="va-h6">Reference model (optional)</h2>
            <p class="va-text-secondary">Choose the model source referenced in this model. This step cannot be undone.</p>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaSelect v-model="refModel" clearable :options="models" :rules="rules">
            </VaSelect>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{
    models: string[],
    referenceModel?: string,
    rules: any[]
}>()

const emits = defineEmits(['change'])


const refModel = computed({
    get() {
        return props.referenceModel
    },
    set(v: string | undefined) {
        emits('change', v)
    }
})

</script>