<template>
    <VaButton color="secondary" :disabled="!projectStore.currentProject.project_id"
        @click="createAndDownloadYaml" icon="download">
        Download YAML
    </VaButton>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../../../../stores/project-store';
import * as YAML from 'yaml';

const projectStore = useProjectStore()

function createAndDownloadYaml() {
    const yaml = YAML.stringify(projectStore.currentProject)
    const blob = new Blob([yaml], { type: 'text/yaml' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.download = projectStore.currentProject.project_id + '.yaml';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

</script>