<template>
    <va-data-table :items="items" :columns="columns">
        <template #headerAppend>
            <tr class="table-crud__slot">
                <th v-for="c in columns" class="p-1">
                    <VaButton block v-if="c === 'actions'" :round="false" @click="$emit('newClicked')" icon="add">
                        New Item</VaButton>
                </th>
            </tr>
        </template>
        <template #cell(actions)="{ rowIndex }">
            <VaButton preset="plain" icon="edit" @click="$emit('editClicked', rowIndex)" />
            <VaButton preset="plain" icon="delete" color="danger" class="ml-3" @click="$emit('deleteClicked', rowIndex)" />
        </template>
    </va-data-table>
</template>
<script setup lang="ts">

const emits = defineEmits(['editClicked', 'deleteClicked'])
const props = defineProps<{
    columns: string[]
    items: Record<string, any>[],
}>()

</script>