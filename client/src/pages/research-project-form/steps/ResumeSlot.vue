<template>
    <ProjectDetails :project="project"/>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useProjectStore } from '../../../stores/project-store';
import ProjectDetails from '../../../components/project/ProjectDetails.vue';


const projectStore = useProjectStore()

const project = computed(() => projectStore.projectForm)

</script>
