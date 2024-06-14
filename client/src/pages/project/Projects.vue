<template>
    <div>
        <div class="row align-end justify-space-between">
            <div class="flex">
                <h1 class="va-h1">Projects</h1>
                <p style="margin-bottom: 6px" class="va-text-secondary">List of projects</p>
            </div>
            <div class="flex">
                <VaButton :to="{ name: 'project-form' }" color="success">Create new
                    project
                </VaButton>
            </div>
        </div>
        <VaDivider style="margin-top: 0;" />
        <div class="row">
            <div class="flex">
                <b>Total:</b> {{ projects.length }}
            </div>
        </div>
        <va-data-table :items="projects" :columns="['name', 'description', 'version', 'action']">
            <template #cell(action)="{ rowData }">
                <va-chip size="small" @click="useProject(rowData as SchemaForm)">
                    View details
                </va-chip>
            </template>
        </va-data-table>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import { useRouter } from 'vue-router';
import { useSchemaStore } from '../../stores/schemas-store';
import { SchemaForm } from '../../data/types';

const projects = ref<Record<string, any>[]>([])

const router = useRouter()
const schemaStore = useSchemaStore()

onMounted(async () => {
    const { data } = await ProjectService.getProjects({})
    projects.value = data.data
})

function useProject(project: SchemaForm) {
    schemaStore.schema = { ...project }
    router.push({ name: 'project', params: { projectId: project.project_id } })
}

</script>