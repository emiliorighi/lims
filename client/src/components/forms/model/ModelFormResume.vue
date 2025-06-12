<template>
    <VaCard>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h2 class="va-h3">
                        Resume
                    </h2>
                    <p class="va-text-secondary">Review and submit the model</p>
                </div>
            </div>
            <div v-if="onlyTextAttributes" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard message="This model has only text attributes, are you sure you want to continue?"
                        icon="fa-warning" color="warning" />
                </div>
            </div>
            <div v-if="duplicatedRefIDAttribute" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard
                        :message="`This model has duplicated attributes in the reference model: ${duplicatedRefIDAttribute}`"
                        icon="fa-warning" color="warning" />
                </div>
            </div>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <ModelDetailsCard :model="modelValue" :title="modelValue.name" />
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>

<script setup lang="ts">
import { ResearchModel } from '../../../data/types'
import ModelDetailsCard from '../../cards/ModelDetailsCard.vue'
import { computed } from 'vue'
import AlertCard from '../../cards/AlertCard.vue'

const props = defineProps<{
    modelValue: ResearchModel,
    sourceModel?: ResearchModel
}>()

const onlyTextAttributes = computed(() => props.modelValue.fields.every(f => f.type === 'text'))
const attributes = computed(() => props.modelValue.fields.map(f => f.key))
const duplicatedRefIDAttribute = computed(() => props.sourceModel?.id_format.find(f => attributes.value.includes(f)))

</script>