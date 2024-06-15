<template>
    <div>
        <h1 class="va-h1 mb-2">
            {{ schemaStore.schema.project_id }}
        </h1>
        <p> <b>Name:</b> {{ schemaStore.schema.name }}</p>
        <p> <b>Version:</b> {{ schemaStore.schema.version }}</p>
        <p> <b>Description:</b> {{ schemaStore.schema.description }}</p>
        <div class="row justify-space-between">
            <!-- <div class="flex lg4 md4 sm12 xs12">
                <ProjectOverviewCard :metadata="schemaStore.schema" />
            </div> -->
            <div class="flex lg4 md4 sm12 xs12">
                <VaCard stripe stripe-color="success">
                    <VaCardContent>
                        <h2 class="va-h4">Samples: {{ lookupData.samples }}</h2>
                    </VaCardContent>
                    <VaCardActions align="between">
                        <VaButton :to="{ name: 'samples', params: { projectId: projectId } }">View</VaButton>
                        <VaButton color="secondary" icon="upload">Upload</VaButton>
                    </VaCardActions>
                </VaCard>
            </div>
            <!-- <div class="flex">
                <VaCard color="secondary">
                    <VaCardContent>
                        <div class="row">
                            <div class="flex">
                                <h2 class="va-h4 ma-0" style="color: white">Experiments {{ lookupData.experiments }}
                                </h2>
                            </div>
                            <div class="flex">
                                <va-chip :to="{ name: 'experiments', params: { projectId: projectId } }">view</va-chip>
                            </div>
                        </div>
                    </VaCardContent>
                </VaCard>
            </div> -->
        </div>

    </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import ProjectService from '../../services/clients/ProjectService';

const schemaStore = useSchemaStore()
const props = defineProps<{
    projectId: string
}>()
const lookupData = ref({ samples: 0, experiments: 0 })

onMounted(async () => {
    const { data } = await ProjectService.getProject(props.projectId)
    schemaStore.schema = { ...data }
    const response = await ProjectService.lookupProject(props.projectId)
    const { samples, experiments } = response.data
    lookupData.value = { samples, experiments }
})

</script>