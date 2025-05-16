<template>
    <VaModal v-model="projectStore.showArchiveModal" close-button hide-default-actions>
        <template #header>
            <h3 class="va-h3">
                {{ header }} {{ projectId }}
            </h3>
            <p class="va-text-secondary">{{ description }}</p>
        </template>
        <VaDivider />
        <template #footer>
            <div class="row justify-space-between">
                <div class="flex">
                    <VaButton :loading="loading" @click="archiveProject" color="warning">{{ btnLabel }}</VaButton>
                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useToast } from 'vuestic-ui/web-components';
import AuthService from '../../services/clients/AuthService';
import { catchError } from '../../composables/toastMessages';
import { useProjectStore } from '../../stores/project-store';

const props = defineProps<{
    projectId: string,
    archive: boolean,
}>()


const { init } = useToast()
const projectStore = useProjectStore()
const loading = ref(false)

const projectStateText = computed(() => {
    return props.archive
        ? {
            header: 'Archiving project',
            btnLabel: 'Archive Project',
            description: 'When a project is archived, it becomes read-only. You can still view all its details and history, but editing, updating, or uploading new content will be disabled until the project is unarchived.',
            request: AuthService.archiveProject
        }
        : {
            header: 'Activating project',
            btnLabel: 'Activate Project',
            description: 'When a project is unarchived, it returns to editable mode. You will be able to update its details, upload new content, and make any necessary changes.',
            request: AuthService.unarchiveProject
        }
})

const header = computed(() => projectStateText.value.header)
const btnLabel = computed(() => projectStateText.value.btnLabel)
const description = computed(() => projectStateText.value.description)
const request = computed(() => projectStateText.value.request)

async function archiveProject() {
    try {
        loading.value = true
        const { data } = await request.value(props.projectId)
        init({ message: data.message })
    } catch (err) {
        catchError(err)
    } finally {
        loading.value = false
        await projectStore.getProjectSchema(props.projectId)
        await projectStore.getProjectStatus(props.projectId)
        projectStore.showArchiveModal = !projectStore.showArchiveModal
    }
}

</script>