<template>
    <div class="row align-center justify-center">
        <div class="flex">
            <VaPagination v-model="offSet" :page-size="limit" :total="total" :visible-pages="3"
                buttons-preset="secondary" rounded gapped border-color="primary"
                @update:model-value="(v: number) => $emit('offsetChanged', v)" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';


const props = defineProps<{
    offset: number,
    limit: number,
    total: number
}>()

const offSet = computed({
    get() {
        return props.offset + 1
    },
    set(v) { 
        emits('offsetChanged', v)
    }
})

const emits = defineEmits(['offsetChanged'])

</script>