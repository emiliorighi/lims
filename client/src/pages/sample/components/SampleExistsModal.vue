<template>
    <div>
        <VaModal hide-default-actions :v-model="sampleStore.overwriteConfirm">
            <template #header>
                <h2 class="va-h2">
                    Sample {{ existingSample?.sample_id }} already exists!
                </h2>
            </template>
            <VaDivider />
            <div class="row justify-space-between">
                <div class="flex">
                    <VaButton @click="updateSample" color="warning">Overwrite</VaButton>
                </div>
                <div class="flex">
                    <VaButton @click="existingSample = undefined" color="secondary">Return</VaButton>
                </div>
            </div>
        </VaModal>
    </div>
</template>
<script setup lang="ts">



</script>