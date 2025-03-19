<template>
    <div>
        <div class="row">
            <div class="flex">
                <h1 class="va-h1">Project Details</h1>
            </div>
        </div>
        <div class="row">
            <div class="flex lg3 md4 sm12 xs12">
                <div class="row">
                    <div v-for="item in modelCounts" class="flex lg12 md12 sm12 xs12">
                        <VaCard>
                            <VaCardContent>
                                <div class="row align-center justify-space-between">
                                    <div class="flex">
                                        <h2 class="va-h3 va-text-capitalize">{{ item.name }}</h2>
                                    </div>
                                    <div class="flex" v-if="item.isSource">
                                        <VaChip size="small" color="backgroundElement">source</VaChip>
                                    </div>
                                </div>
                            </VaCardContent>
                            <VaCardContent>
                                <div class="row align-center justify-space-between">
                                    <div class="flex">
                                        <Counter :duration="2000" :target-value="item.counts" />
                                        <p> Records
                                        </p>
                                    </div>
                                    <div class="flex">
                                        <VaButton preset="secondary" color="textPrimary">View Records</VaButton>
                                    </div>
                                </div>
                            </VaCardContent>
                        </VaCard>
                    </div>
                </div>
            </div>
            <div class="flex lg9 md8 sm12 xs12">
                <VaCard v-if="schemaStore.schema">
                    <VaCardContent>
                        <div class="row align-center justify-space-between">
                            <div class="flex">
                                <h2 class="va-h3">Project Schema</h2>
                            </div>
                            <div class="flex">
                                <ProjectYamlButton :file-name="projectId" color="textPrimary" preset="primary"
                                    :project="schemaStore.schema" />
                            </div>
                        </div>
                    </VaCardContent>
                    <VaCardContent>
                        <ProjectDetails :project="schemaStore.schema" />
                    </VaCardContent>
                </VaCard>
            </div>
        </div>
    </div>

</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import Counter from '../../components/ui/Counter.vue';
import ProjectDetails from '../../components/project/ProjectDetails.vue';
import { useSchemaStore } from '../../stores/schema-store';
import ProjectYamlButton from '../../components/project/ProjectYamlButton.vue';

const props = defineProps<{
    projectId: string
}>()

const schemaStore = useSchemaStore()
const models = computed(() => schemaStore.schema?.models ?? [])
const modelCounts = ref<{ name: string, counts: number, isSource: boolean }[]>([])

onMounted(async () => await getProjectStats())

async function getProjectStats() {
    const { data } = await ProjectService.lookupProject(props.projectId)
    modelCounts.value = [
        ...Object.entries(data).map(([k, v]) => ({ name: k, counts: v as number, isSource: !models.value.find(m => m.name === k)?.reference_model }))
    ]
}


</script>