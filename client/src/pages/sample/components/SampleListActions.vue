<template>
    <div class="row">
        <div class="flex">
            <VaButton @click="newSample" icon="add">Sample</VaButton>
        </div>
        <div class="flex">
            <VaButton @click="tsvUpload" icon="upload">TSV</VaButton>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSampleStore } from '../../../stores/sample-store';

const emit = defineEmits(['newSample', 'tsvUpload']);

const sampleStore = useSampleStore()

function newSample() {
    sampleStore.initSample()
    sampleStore.showForm = true
}

function tsvUpload() {
    
}
</script>