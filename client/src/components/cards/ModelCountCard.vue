<template>
    <VaCard class="card">
        <VaCardContent>
            <div class="row justify-space-between align-center">
                <div class="flex">
                    <Counter :duration="2000" :target-value="card.count" />
                    <p>
                        {{ card.text }}
                    </p>
                </div>
                <div class="flex">
                    <VaIcon :color="card.color" :name="card.icon" size="large"></VaIcon>
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import Counter from '../ui/Counter.vue'

const props = defineProps<{
    card: {
        color: string
        icon: string
        count: number
        text: string
    }
}>()


</script>
<style scoped>
.card {
    flex: 1;
    display: flex;
    flex-direction: column;
}
</style>