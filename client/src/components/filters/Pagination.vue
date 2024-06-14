<template>
    <va-pagination v-model="offset" :page-size="limit" :total="total" :visible-pages="3" buttons-preset="secondary"
        rounded gapped border-color="primary" @update:model-value="(v: number) => $emit('offsetChanged', v)" />
</template>
<script setup lang="ts">
import { ref } from 'vue';


const props = defineProps<{
    offSet: number,
    limit: number,
    total: number
}>()

const offset = ref(props.offSet + 1)

const emits = defineEmits(['offsetChanged'])

</script>