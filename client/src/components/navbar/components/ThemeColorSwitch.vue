<template>
    <div class="row" style="width: min-content;">
        <div class="flex lg12 md12 sm12 xs12">
            Primary color:
            <VaColorPalette class="mt-2 mb-2" v-model="colors.primary" :palette="palette" />
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            Dark mode:
            <VaSwitch class="mt-2 mb-2" v-model="switchValue" true-value="dark" false-value="light" size="small" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useColors } from "vuestic-ui";

const { applyPreset, currentPresetName, colors } = useColors();

const palette = ["#2c82e0", "#ef476f", "#ffd166", "#06d6a0", "#8338ec"];

const switchValue = computed({
    get() { return currentPresetName.value },
    set(value) { applyPreset(value) }
})
</script>