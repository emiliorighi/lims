<template>
    <div class="row align-center justify-space-between">
        <div class="flex">
            <b>Total {{ total }}</b>
            Results per page
            <VaSelect style="width: 100px;" :options="[10, 20, 50]" v-model="limit"
                @update:modelValue="(v: number) => $emit('handleLimit', v)" />
        </div>
        <div class="flex">
            <VaPagination v-model="offSet" :page-size="limit" :total="total" :visible-pages="3"
                buttons-preset="secondary" rounded gapped border-color="primary"
                @update:model-value="(v: number) => $emit('offsetChanged', v)" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';


const props = defineProps<{
    offset: number,
    limit: number,
    total: number
}>()

// const offSet = ref(props.offset + 1)

const offSet = computed({
    get() {
        return props.offset + 1
    },
    set(v) { 
        emits('offsetChanged', v)
    }
})

const emits = defineEmits(['offsetChanged', 'handleLimit'])

</script>