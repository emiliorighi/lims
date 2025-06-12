<template>
    <VaCard stripe :stripe-color="color">
        <VaCardContent>
            <div class="row align-center">
                <div class="flex">
                    <VaIcon :name="icon" :color="color" />
                </div>
                <div class="flex">
                    <h3 class="va-h6">
                        {{ message }}
                    </h3>
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">

const props = defineProps<{
    message: string
    icon: string
    color: string
}>()


</script>