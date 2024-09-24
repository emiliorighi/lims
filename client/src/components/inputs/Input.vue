<template>
    <VaInput :type="type" v-model="filter" clearable :label="label">
    </VaInput>
</template>
<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
    label: string,
    type: string,
    value?: string
}>()

const filter = computed({
    get() {
        return props.value ? props.value : ''
    },
    set(v: any) {
        emits('valueChange', v);
    }
})

const emits = defineEmits(['valueChange'])

</script>