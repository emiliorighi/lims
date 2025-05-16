<template>
    <div style="max-height: 150px; overflow: scroll;">
        <VaOptionList v-model="modelValue" :options="props.choices" />
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{ value: string | null; choices: string[] }>();
const emit = defineEmits(['update:value']);

const modelValue = computed({
    get: () => {
        if (props.value)
            return props.value.split(',')
        return []
    },
    set: (val: string[]) => emit('update:value', val.length > 0 ? val.join(',') : null),
});
</script>