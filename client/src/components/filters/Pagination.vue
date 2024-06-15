<template>
    <va-pagination v-model="offSet" :page-size="limit" :total="total" :visible-pages="3" buttons-preset="secondary"
        rounded gapped border-color="primary" @update:model-value="(v: number) => $emit('offsetChanged', v)" />
</template>
<script setup lang="ts">
import { ref } from 'vue';


const props = defineProps<{
    offset: number,
    limit: number,
    total: number
}>()

const offSet = ref(props.offset + 1)

const emits = defineEmits(['offsetChanged'])

</script>