<template>
    <div>
        <h1 class="va-h1">{{ title }}</h1>
        <p style="margin-bottom: 6px" class="va-text-secondary">
            {{ description }}</p>
    </div>
</template>
<script setup lang="ts">
const props = defineProps<{
    title: string,
    description: string
}>()


</script>