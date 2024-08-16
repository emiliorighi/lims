<template>
    <router-view v-if="showProject"></router-view>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useSchemaStore } from '../stores/schemas-store';
import ProjectService from '../services/clients/ProjectService';

const schemaStore = useSchemaStore()
const props = defineProps<{
    projectId: string
}>()


const showProject = computed(() => {
    return !!schemaStore.schema.project_id
})

onMounted(async () => {
    if (!showProject.value) await getProject()
})

async function getProject() {
    try {
        const { data } = await ProjectService.getProject(props.projectId)
        schemaStore.schema = { ...data }
    } catch (error) {
        console.error(error)
    }
}
</script>