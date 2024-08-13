<template>
    <div class="row align-center justify-space-between">
        <div class="flex">
            <b>Total {{ total }}</b>
            Results per page
            <VaSelect style="width: 100px;" :options="[10, 20, 50]" v-model="limit"
                @update:modelValue="(v: number) => $emit('handleLimit', v)" />
        </div>
        <div class="flex">
            <va-pagination v-model="offSet" :page-size="limit" :total="total" :visible-pages="3"
                buttons-preset="secondary" rounded gapped border-color="primary"
                @update:model-value="(v: number) => $emit('offsetChanged', v)" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';


const props = defineProps<{
    offset: number,
    limit: number,
    total: number
}>()

const offSet = ref(props.offset + 1)

const emits = defineEmits(['offsetChanged', 'handleLimit'])

</script>