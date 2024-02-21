<template>
    <div>
        <h1 class="va-h1">
            {{ schemaStore.schema.project_id }}
        </h1>
        <p> <b>Name:</b> {{ schemaStore.schema.name }}</p>
        <p> <b>Version:</b> {{ schemaStore.schema.version }}</p>
        <p v-if="schemaStore.schema.description"> <b>Description:</b> {{ schemaStore.schema.description }}</p>
        <div class="row justify-center">
            <div class="flex">
                <va-card color="success">
                    <va-card-content>
                        <div class="row">
                            <div class="flex">
                                <h2 class="va-h4 ma-0" style="color: white">Samples</h2>
                            </div>
                            <div class="flex">
                                <va-chip :to="{name:'samples'}">view</va-chip>
                            </div>
                        </div>
                    </va-card-content>
                </va-card>
            </div>
            <div class="flex">
                <va-card color="scondary">
                    <va-card-content>
                        <div class="row">
                            <div class="flex">
                                <h2 class="va-h4 ma-0" style="color: white">Experiments</h2>
                            </div>
                            <div class="flex">
                                <va-chip :to="{name:'experiments'}">view</va-chip>
                            </div>
                        </div>
                    </va-card-content>
                </va-card>

            </div>
        </div>
        <!-- <va-tabs grow v-model="tab">
            <template #tabs>
                <va-tab v-for="t in ['samples', 'experiments']" :key="t" :name="t">
                    {{ t }}
                </va-tab>
            </template>
        </va-tabs>
        <va-divider /> -->
        <router-view v-if="schemaStore.schema.project_id"></router-view>
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

const tab = ref('samples')
onMounted(async () => {
    const { data } = await ProjectService.getProject(props.projectId)
    schemaStore.schema = { ...data }
})

</script>