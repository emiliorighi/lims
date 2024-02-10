<template>
    <VaCard stripe :stripe-color="isModelIdValid ? 'success' : 'danger'">
        <VaCardContent v-if="isModelIdValid">
            Selected keys (click to unselect):
            <VaChip v-for="item in projectStore.project[model].id_format" :key="item" class="ml-2"
                @click="unselectIdKey(item)">
                {{ item }}
            </VaChip>
            <p> Id format preview: <b>{{ projectStore.project[model].id_format.join('_') }}</b>
            </p>
        </VaCardContent>
        <VaCardContent v-else>
            <p>1. Select at leas one attribute key that will be used as the id of {{ model }}</p>
            <p v-if="projectStore.project[model].fields.length === 0">2. Create at least one attribute</p>
        </VaCardContent>
        <VaCardContent>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useProjectStore } from '../../../stores/project-store';

const props = defineProps<{
    model: 'sample' | 'experiment'
}>()
const isModelIdValid = computed(() => {
    return projectStore.project[props.model].id_format.length > 0
})
const projectStore = useProjectStore()

function unselectIdKey(item: string) {
    projectStore.project[props.model].id_format = [...projectStore.project[props.model].id_format.filter(
        (selectedItem) => selectedItem !== item
    )]
}
</script>