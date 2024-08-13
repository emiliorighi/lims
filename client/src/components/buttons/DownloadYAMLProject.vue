<template>
    <VaButton border-color="primary" preset="secondary" :disabled="!project.project_id" @click="createAndDownloadYaml"
        icon="download">
        YAML Schema
    </VaButton>
</template>
<script setup lang="ts">
import { SchemaForm } from '../../data/types'
import * as YAML from 'yaml';


const props = defineProps<{
    project: SchemaForm
}>()

function createAndDownloadYaml() {
    const yaml = YAML.stringify(props.project)
    const blob = new Blob([yaml], { type: 'text/yaml' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.download = props.project.project_id + '.yaml';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

</script>