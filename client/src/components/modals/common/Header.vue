<template>
    <div class="row align-center justify-space-between">
        <div class="flex">
            <h3 class="va-h3">
                {{ title }}
            </h3>
            <p v-if="description" class="va-text-secondary">{{ description }}</p>
        </div>
        <VaIcon v-if="icon" color="primary" size="large" class="flex" :name="icon" />
    </div>
</template>

<script setup lang="ts">

const props = defineProps<{
    title: string
    description?: string
    icon?: string
}>()

</script>