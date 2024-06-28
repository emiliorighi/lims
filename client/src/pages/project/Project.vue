<template>
    <div>
        <h1 class="va-h1 mb-2">
            {{ projectId }}
        </h1>
        <div class="row">
            <div class="flex">
                <VaButton :to="{ name: 'samples', params: { projectId: projectId } }" icon="fa-vial" color="success">
                    Samples {{ lookupData.samples }}</VaButton>
            </div>
            <div class="flex">
                <VaButton :to="{ name: 'experiments', params: { projectId: projectId } }" icon="fa-dna">Experiments {{
                lookupData.experiments }}</VaButton>
            </div>
        </div>
        <div v-if="showProject" class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <ProjectOverviewCard :metadata="schemaStore.schema" />
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import ProjectService from '../../services/clients/ProjectService';
import ProjectOverviewCard from '../../components/project/ProjectOverviewCard.vue';

const schemaStore = useSchemaStore()
const props = defineProps<{
    projectId: string
}>()
const lookupData = ref({ samples: 0, experiments: 0 })


const showProject = computed(() => {
    return !!schemaStore.schema.project_id
})

onMounted(async () => {
    if (!schemaStore.schema.project_id) await getProject()
    await getData()
})


async function getProject() {
    try {
        const { data } = await ProjectService.getProject(props.projectId)
        schemaStore.schema = { ...data }
    } catch (error) {
        console.error(error)
    }
}

async function getData() {
    try {
        const response = await ProjectService.lookupProject(props.projectId)
        const { samples, experiments } = response.data
        lookupData.value = { samples, experiments }
    } catch (error) {
        console.error(error)
    }
}

</script>