<template>
    <VaCard>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h2 class="va-h3">Identifiers</h2>
                    <p class="va-text-secondary">Choose the combination of attributes that define the identifier. The
                        order
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
                            <VaChip color="success" v-for="chip in value" :key="chip" size="small" class="mr-1 my-1"
                                closeable @update:model-value="id_format = id_format.filter(f => f !== chip)">
                                {{ chip }}
                            </VaChip>
                        </template>
                    </VaSelect>
                </div>
            </div>
            <div v-if="modelId.length" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <IdFormatPreviewCard :model-name="modelName" :model-id="modelId" :ref-model="refModel"
                        :ref-model-id-fields="refModelIdFields" />
                </div>
            </div>
            <div v-if="duplicatedRefModelIdFields?.length" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard
                        :message="`The following attributes are duplicated in the reference model: ${duplicatedRefModelIdFields.join('_')}`"
                        icon="fa-warning" color="warning" />
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import AlertCard from '../cards/AlertCard.vue'
import IdFormatPreviewCard from '../cards/IdFormatPreviewCard.vue'

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

const duplicatedRefModelIdFields = computed(() => props.refModelIdFields?.filter(f => props.attributes.includes(f)))


</script>
<style scoped>
.ml-1 {
    margin-left: 0.5rem;
}

.identifier-preview {
    background-color: var(--va-background-element);
}

.ref-model-id {
    color: var(--va-primary);
}

.model-id {
    color: var(--va-success);
}
</style>