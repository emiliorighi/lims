<template>
    <VaCard stripe :stripe-color="color" class="flex lg12 md12 sm12 xs12">
        <VaCardContent>
            {{ text }}
        </VaCardContent>
        <VaCardActions>
            <VaButton @click="setIncomingProject(existingProject)">Upload Project</VaButton>
        </VaCardActions>
    </VaCard>
</template>
<script setup lang="ts">
import { SchemaForm } from './../../data/types'
import { useProjectStore } from './../../stores/project-store'


const projectStore = useProjectStore()

const props = defineProps<{
    id: string,
    existingProject: SchemaForm,
    color: string,
    text: string
}>()

function setIncomingProject(project: SchemaForm) {
    if (project.created) {
        const { created, ...d } = project
        projectStore.incomingProject = { ...d }
    } else {
        projectStore.incomingProject = { ...project }
    }
    projectStore.switchConfirm()

}
</script>