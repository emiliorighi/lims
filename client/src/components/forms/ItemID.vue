<template>
    <h6 class="va-h6">Generated ID</h6>
    <p class="va-text-secondary mb-2">This section displays the generated ID</p>
    <div class="row">
        <div class="flex lg6 md6 sm12 xs12 mb-2">
            <VaInput readonly label="Unique identifier" v-model="id"
                placeholder="The unique identifier will be generated here" :rules="rules">
            </VaInput>
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    id: string
    rules: any
}>()

</script>