<template>
    <VaCard color="backgroundElement">
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h4 class="va-h6">
                        How your record identifiers will be constructed:
                    </h4>
                </div>
            </div>
            <div v-if="refModelIdFields" class="row align-center">
                <div class="flex">
                    <span class="va-text-secondary">
                        Inherited from {{ refModel }}:
                    </span>
                </div>
                <div class="flex">
                    <VaChip color="primary" size="small" class >
                        {{ refModelIdFields.join('_') }}_
                    </VaChip>
                </div>
            </div>
            <div class="row align-center">
                <div class="flex">
                    <span class="va-text-secondary">
                        {{ modelName }}'s identifiers:
                    </span>
                </div>
                <div class="flex">
                    <VaChip v-for="field in modelId" :key="field" color="success" size="small" class="mr-2" >
                        {{ field }}
                    </VaChip>
                </div>
            </div>
            <VaDivider/>
            <div class="row">
                <div class="flex">
                    <p class="va-text-secondary">
                        Final identifier format:
                    </p>
                </div>
            </div>
            <div class="row">
                <div class="flex">
                    <VaCard class="identifier-preview va-text-bold">
                        <VaCardContent>
                            <span v-if="refModelIdFields" class="ref-model-id">
                                {{ refModelIdFields.join('_') }}_
                            </span>
                            <span class="model-id">
                                {{ modelId.join('_') }}
                            </span>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <VaAlert color="info" outline icon="fa-info-circle">
                <p>The attributes used for the identifier will be saved as required</p>
            </VaAlert>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">

const props = defineProps<{
    modelName: string,
    modelId: string[],
    refModel?: string,
    refModelIdFields?: string[],
}>()


</script>
<style scoped>

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