<template>
    <div class="row">
        <div class="flex">
            <h3 class="va-h3">Identifiers</h3>
            <p class="va-text-secondary">Choose the combination of attributes that define the identifier. The order
                selection
                matters! The identifier is the value the uniquely defines each row of your TSV
                or
                spreadsheet, it can be one attribute or the combination or more attributs</p>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaSelect multiple v-model="id_format" :disabled="props.disabled" :options="attributes" :rules="[
                (v: any) => v.length > 0 || 'Choose at least one field',
                (v: any) => v.every((a: any) => attributes.includes(a)) || 'Some choosen attributes are not present in the attribute list'
            ]">
                <template #content="{ value }">
                    <VaChip color="success" v-for="chip in value" :key="chip" size="small" class="mr-1 my-1" closeable
                        @update:model-value="id_format = id_format.filter(f => f !== chip)">
                        {{ chip }}
                    </VaChip>
                </template>
            </VaSelect>
        </div>
    </div>
    <div v-if="modelId.length" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard color="backgroundElement">
                <VaCardTitle>
                    Identifier preview
                </VaCardTitle>
                <VaCardContent>
                    <div v-if="refModelIdFields" class="row">
                        <div class="flex">
                            <VaChip color="primary" size="small">{{ refModel }}'s identifiers </VaChip>
                        </div>
                        <div class="flex">
                            <VaChip color="success" size="small">{{ modelName }}'s identifiers </VaChip>
                        </div>
                    </div>
                    <h4 class="va-h4">
                        <span style="color:var(--va-primary)" v-if="refModelIdFields">{{ refModelIdFields.join('_')
                        }}_</span><span style="color: var(--va-success);">{{
                                modelId.join('_') }}</span>
                    </h4>
                </VaCardContent>
                <VaCardContent>
                    <p>NOTE: The attributes used for the identifier will be saved as required</p>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    attributes: string[],
    modelName: string,
    modelId: string[],
    refModel?: string,
    refModelIdFields?: string[],
    disabled?: boolean
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