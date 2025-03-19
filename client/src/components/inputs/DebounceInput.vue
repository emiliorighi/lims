<template>
    <VaInput v-model="model" :placeholder="placeholder" :rules="rules" :label="label" />
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { debounce } from '../../composables/debounce';

const props = defineProps<{
    parentModel: string,
    label?: string,
    placeholder?: string,
    rules?: any[]
}>()

const emits = defineEmits(['change'])


const debouncedEmit = debounce((payload: any) => {
    emits('change', payload);
}, 200);

const model = computed({
    get() {
        return props.parentModel
    },
    set(v: string) {
        debouncedEmit(v)
    }
})



</script>