<!-- src/components/Sidebar.vue -->
<template>
    <transition name="slide">
        <div v-if="isOpen" class="sidebar">
            <slot></slot>
        </div>
    </transition>
</template>

<script setup lang="ts">
const props = defineProps<{
    isOpen: boolean
}>()
</script>

<style scoped>
.sidebar {
    width: 250px;
    height: 100vh;
    background-color: #2c3e50;
    position: fixed;
    top: 0;
    left: 0;
    overflow: hidden;
    transition: transform 0.3s ease;
}

/* Transition for the slide */
.slide-enter-active,
.slide-leave-active {
    transition: transform 0.3s ease;
}

.slide-enter-from {
    transform: translateX(-100%);
}

.slide-leave-to {
    transform: translateX(-100%);
}
</style>