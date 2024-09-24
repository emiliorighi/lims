<template>
    <VaInput v-model="minValue" :label="label + ' min'" strict-bind-input-value>

    </VaInput>
    <VaInput v-model="maxValue" :label="label + ' max'" strict-bind-input-value>

    </VaInput>
</template>
<script setup lang="ts">
import { computed, reactive,} from 'vue';
import { debounce } from '../../composables/debounce'

const props = defineProps<{
    max: number,
    min: number
    label: string
}>()

const emits = defineEmits(['valueChange'])

const range = reactive({
    minValue: 0,
    maxValue: 0
})

const debouncedEmit = debounce((value: number[]) => {
    emits('valueChange', value);
}, 200);


const minValue = computed({
    get() {
        return props.min
    },
    set(v: number) {

    }
})

const maxValue = computed({
    get() {
        return props.max
    },
    set(v: number) {

    }
})
</script>