<template>
    <VaCard stripe :stripe-color="modelId.length > 0 ? 'success' : 'danger'">
        <VaCardContent v-if="modelId.length > 0">
            Selected keys (click to unselect):
            <VaChip v-for="item in projectStore.currentProject[model].id_format" :key="item" class="ml-2"
                @click="unselectIdKey(item)">
                {{ item }}
            </VaChip>
            <p class="mt-4"> Id format preview: <b>{{ projectStore.currentProject[model].id_format.join('_') }}</b>
            </p>
        </VaCardContent>
        <VaCardContent v-else>
            <p>1. Select at least one filter key that will be used as the id of {{ model }}! </p>
        </VaCardContent>
        <VaCardContent>
            IMPORTANT: The attributes used as id
            will be stored as required!
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useProjectStore } from './../../stores/project-store';

const props = defineProps<{
    model: 'sample' | 'experiment'
}>()
const modelId = computed(() => {
    return projectStore.currentProject[props.model].id_format
})
const projectStore = useProjectStore()

function unselectIdKey(item: string) {
    projectStore.currentProject[props.model].id_format = [...projectStore.currentProject[props.model].id_format.filter(
        (selectedItem) => selectedItem !== item
    )]
}

</script>