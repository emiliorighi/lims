<template>
    <VaInput :loading="loading" v-model="model" @input="emits('input')" :placeholder="placeholder" :rules="rules"
        :label="label" :clearable="clearable">
        <template #prependInner>
            <VaIcon v-if="icon" :name="icon" />
        </template>
    </VaInput>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { debounce } from '../../composables/debounce';

const props = defineProps<{
    parentModel: string,
    label?: string,
    placeholder?: string,
    clearable?: boolean,
    icon?: string,
    loading?: boolean
    rules?: any[]
}>()

const emits = defineEmits(['change', 'input'])


const debouncedEmit = debounce((payload: any) => {
    emits('change', payload);
}, 350);



const model = computed({
    get() {
        return props.parentModel
    },
    set(v: string) {
        debouncedEmit(v)
    }
})



</script>