<template>
    <h1 class="va-h1">{{ schemaStore.schema.project_id }}</h1>
    <div class="row justify-space-between align-end">
        <div class="flex lg6 md8 sm8 xs8">
            <VaTabs v-model="tab">
                <template #tabs>
                    <VaTab name="samples" label="Samples" icon="fa-vial" />
                    <VaTab v-if="schemaStore.schema.experiment.id_format.length" name="experiments" label="Experiments"
                        icon="fa-dna" />
                    <VaTab v-if="isAuthorized" name="upload" label="Upload" icon="upload_file" />
                </template>
            </VaTabs>
        </div>
        <div class="flex">
            <div class="row">
                <div class="flex">
                    <VaButton @click="schemaStore.showChart = !schemaStore.showChart">Create Chart</VaButton>
                </div>
                <div class="flex">
                    <VaButton preset="primary" @click="schemaStore.showSchema = !schemaStore.showSchema">
                        View Schema
                    </VaButton>
                </div>
            </div>
        </div>
    </div>
    <div v-if="schemaStore.schema.project_id">
        <Upload v-if="tab === 'upload'" />
        <Items v-else :button-label="selectedProps.buttonLabel" :model="selectedProps.model"
            :icon="selectedProps.icon" />
    </div>
    <Statistics />
    <ProjectDetailsModal />
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import ProjectService from '../../services/clients/ProjectService';
import ProjectDetailsModal from '../../components/modals/ProjectDetailsModal.vue'
import Items from './children/Items.vue';
import { ModelType } from '../../data/types';
import Upload from './children/Upload.vue';
import Statistics from './children/Statistics.vue';
import { useGlobalStore } from '../../stores/global-store';

const schemaStore = useSchemaStore()
const globalStore = useGlobalStore()
const props = defineProps<{
    projectId: string
}>()

const isAuthorized = computed(() => {
    return globalStore.isAuthenticated && (globalStore.user.role === 'admin' || globalStore.user.projects.includes(schemaStore.schema.project_id))
})

const tab = ref('samples')

const itemProps = [
    {
        buttonLabel: 'Sample',
        icon: 'fa-vial',
        model: 'sample' as ModelType
    },
    {
        buttonLabel: 'Experiment',
        icon: 'fa-dna',
        model: 'experiment' as ModelType
    },
]

const selectedProps = computed(() => tab.value === 'samples' ? itemProps[0] : itemProps[1])

onMounted(async () => {
    if (!schemaStore.schema.project_id) await getProject()
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