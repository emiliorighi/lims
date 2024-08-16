<template>
    <VaModal max-height="500px" fixed-layout v-model="itemStore.showItemDetails">
        <template #header>
            <div class="row align-center justify-space-between">
                <h3 class=" flex va-h3">
                    {{ itemId }}
                </h3>
                <VaIcon color="primary" size="large" class="flex" :name="icon" />
            </div>
        </template>
        <VaDivider />
        <div v-if="itemStore.item" class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <MetadataTree :metadata="Object.entries(itemStore.item.metadata)" />
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { useItemStore } from '../../stores/item-store';
import MetadataTree from '../ui/MetadataTree.vue';
import { computed } from 'vue'

const props = defineProps<{
    icon: string,
}>()

const itemId = computed(() => {
    if (itemStore.item) {
        return 'experiment_id' in itemStore.item ? itemStore.item.experiment_id : itemStore.item.sample_id
    }
})

const itemStore = useItemStore()

</script>