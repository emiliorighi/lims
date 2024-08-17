<template>
    <span>{{ displayedText }}</span>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps<{
    text: string;
    speed?: number; // Optional, default speed of typing
}>();

const displayedText = ref('');
const currentIndex = ref(0);
const speed = props.speed || 100; // Default typing speed in milliseconds

let typingInterval: number | undefined;

const startTyping = () => {
    typingInterval = window.setInterval(() => {
        if (currentIndex.value < props.text.length) {
            displayedText.value += props.text[currentIndex.value];
            currentIndex.value++;
        } else {
            clearInterval(typingInterval);
        }
    }, speed);
};

onMounted(() => {
    startTyping();
});

onBeforeUnmount(() => {
    if (typingInterval) {
        clearInterval(typingInterval);
    }
});
</script>