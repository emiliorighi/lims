<template>
    <div>
        <div class="row justify-center">
            <div class="flex">
                {{ project.name }}
            </div>
        </div>
        <div class="row justify-space-between">
            <div class="flex">
                <va-button icon="add" @click="router.push({ name: 'sample-form' })">
                    New sample
                </va-button>
            </div>
            <div class="flex">
                <va-button icon="add">
                    New experiment
                </va-button>
            </div>

            <!-- <div class="flex">
                <va-card>
                    <va-card-title class="row">
                        <div class="flex">
                            Samples
                        </div>
                        <va-button class="flex" icon="add"/>
                    </va-card-title>
                    <va-card-content class="row">
                        <va-button></va-button>
                    </va-card-content>
                </va-card>
            </div> -->
        </div>
        <router-view />
    </div>
    <!-- <div class="row">
        <div class="flex lg6 md6 sm12 xs12">
            <va-card>
                <va-card-title>
                    Experiments
                </va-card-title>
                <va-card-actions>
                    <va-button>Create Experiment</va-button>
                </va-card-actions>
                <va-divider/>
                <va-data-table>
                </va-data-table>
            </va-card>
        </div>
        <div class="flex lg6 md6 sm12 xs12">
            <va-card>
                <va-card-title>
                    Samples
                </va-card-title>
                <va-card-actions>
                    <va-button>
                        Create Sample
                    </va-button>
                </va-card-actions>
                <va-divider/>
                <va-data-table>

                </va-data-table>
            </va-card>
        </div>
    </div> -->
</template>
<script setup lang="ts">
import { onMounted } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import { useRouter } from 'vue-router';
import ProjectService from '../../services/clients/ProjectService';

const schemaStore = useSchemaStore()
const router = useRouter()
const project = schemaStore.schema
const props = defineProps<{
    id: string
}>()

onMounted(async () => {
    if (!project.project_id) schemaStore.schema = await ProjectService.getProject(props.id)
})
</script>