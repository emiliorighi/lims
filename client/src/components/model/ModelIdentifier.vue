<template>
    <div class="row">
        <div class="flex">
            <h2 class="va-h6">Model Identifier</h2>
            <p class="va-text-secondary">Choose the attribute(s) that define the identifier. The order selection
                matters! The identifier is the value the uniquely defines each row of your TSV
                or
                spreasheet, it can be one column or the combination or more columns</p>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaSelect multiple v-model="id_format" :options="attributes" :rules="[
                (v: string[]) => v.length > 0 || 'Choose at least one field',
                (v: string[]) => v.every(a => attributes.includes(a)) || 'Some choosen attributes are not present in the attribute list'
            ]">
                <template #content="{ value }">
                    <VaChip v-for="chip in value" :key="chip" size="small" class="mr-1 my-1" closeable
                        @update:model-value="id_format = id_format.filter(f => f !== chip)">
                        {{ chip }}
                    </VaChip>
                </template>
            </VaSelect>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            The identifier will be: <strong> {{ modelId.join('_') }}
            </strong>
            <p>The attributes used for the identifier will be saved as required</p>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
const props = defineProps<{
    attributes: string[],
    modelId: string[],
}>()

const emits = defineEmits(['change'])


const id_format = computed({
    get() {
        return props.modelId
    },
    set(v: string[]) {
        emits('change', v)
    }
})

</script>