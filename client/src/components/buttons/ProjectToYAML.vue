<template>
    <VaButton icon="fa-file-arrow-down" :loading="isLoading" :preset="preset" :color="color"
        @click.stop.prevent="createAndDownloadYaml">
        Download
    </VaButton>
</template>
<script setup lang="ts">
import { ReseachProject } from '../../data/types'
import * as YAML from 'yaml';
import { ref } from 'vue'

const props = defineProps<{
    project: ReseachProject
    fileName: string,
    preset?: string,
    color?: string,
}>()

const isLoading = ref(false)

function createAndDownloadYaml() {
    isLoading.value = true;
    try {
        const yaml = YAML.stringify(props.project);
        const blob = new Blob([yaml], { type: 'text/yaml' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);

        link.href = url;
        link.download = props.fileName + '.yaml';

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error creating or downloading the YAML file:', error);
        // Optionally, you could set an error state or show a notification to the user here
    } finally {
        isLoading.value = false;
    }
}


</script>