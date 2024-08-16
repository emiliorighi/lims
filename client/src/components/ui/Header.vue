<template>
    <h1 class="va-h1">{{ title }}</h1>
</template>
<script setup lang="ts">
const props = defineProps<{
    title: string,
}>()

</script>