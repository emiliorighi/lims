<template>
    <div class="row justify-end">
        <div class="flex">
            <va-button :to="{name:'project-form'}">create project</va-button>
        </div>
    </div>
    <va-divider />
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <va-card>
                <va-data-table :items="projects" :columns="['name', 'description', 'version', 'action']">
                    <template #cell(action)="{ rowData }">
                        <va-button size="small" @click="useProject(rowData)">
                            Select
                        </va-button>
                    </template>
                </va-data-table>
            </va-card>
        </div>
    </div>
    <router-view></router-view>
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
    router.push({ path: `/projects/${project.project_id}`, params: { id: project.project_id } })
}

</script>