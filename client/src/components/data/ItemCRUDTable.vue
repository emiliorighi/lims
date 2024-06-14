<template>
    <va-data-table :items="items" :columns="columns">
        <template #cell(actions)="{ rowIndex }">
            <VaButton preset="plain" icon="edit" @click="$emit('editClicked', rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3" @click="$emit('deleteClicked', rowIndex)" />
        </template>
    </va-data-table>
</template>
<script setup lang="ts">

const emits = defineEmits(['editClicked', 'deleteClicked','newClicked'])
const props = defineProps<{
    columns: string[]
    items: Record<string, any>[],
}>()

</script>