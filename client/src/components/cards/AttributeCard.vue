<template>
    <VaCard>
        <VaCardContent>
            <div class="row justify-end">
                <div class="flex">
                    <VaButton @click="emits('onDelete', index)" color="danger">Remove</VaButton>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaInput label="Attribute name (required)"></VaInput>
                </div>
                <div class="flex lg6 md6 sm12 xs12">
                    <VaSelect label="Attribute type" :options="options"></VaSelect>
                </div>
                <div class="flex">
                    <VaCheckbox label="Required"></VaCheckbox>
                </div>
                <div class="flex">
                </div>
                <div class="flex lg12 m12 sm12 xs12">
                    <VaInput label="Attribute description (optional)"></VaInput>
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { useAttributeStore } from '../../stores/attribute-store';


const attributeStore = useAttributeStore()
const props = defineProps<{
    index: number,
    isTsvUploaded:boolean
}>()

const emits = defineEmits(['onDelete'])
const options = [
    'select',
    'text',
    'date',
    'number'
]


</script>