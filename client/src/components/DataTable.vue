<template>
    <va-data-table :columns="columns" :items="items">

    </va-data-table>
</template>
<script setup lang="ts">
const props = defineProps<{
    columns: string[]
    items: Record<string, any>[]
}>()
</script>