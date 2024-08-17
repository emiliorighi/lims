<template>
    <div class="row mt-4">
        <VaFileUpload class="flex lg12 md12 sm12 xs12" v-model="uploadedTSV" dropzone style="z-index: 0"
            file-types=".tsv" type="single" undo :uploadButtonText="`Upload ${model}s`" />
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ model: string, tsv: any }>();


const uploadedTSV = computed({
    get() {
        return props.tsv
    },
    set(v) {
        emit('update:tsv', v)
    }
})
const emit = defineEmits(['update:tsv']);

</script>