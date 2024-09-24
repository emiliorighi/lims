<template>
    <VaModal max-height="500px" fixed-layout v-model="itemStore.showItemDetails">
        <template #header>
            <Header :title="itemId" :icon="icon" />
        </template>
        <VaDivider />
        <div v-if="item" class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <MetadataTree :metadata="Object.entries(item)" />
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { useItemStore } from '../../stores/item-store';
import MetadataTree from '../ui/MetadataTree.vue';
import { computed } from 'vue'
import Header from './common/Header.vue'

const props = defineProps<{
    icon: string,
}>()

const itemStore = useItemStore()

const model = computed(() => itemStore.currentModel)

const item = computed(() => itemStore.stores[model.value].item)

const itemId = computed(() => {
    if (!item.value) return ''
    return model.value === 'experiment' ? item.value.experiment_id : item.value.sample_id

})

</script>