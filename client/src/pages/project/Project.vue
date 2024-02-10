<template>
    <div>
        <h1 class="va-h1">
            {{ schemaStore.schema.project_id }}
        </h1>
        <p> <b>Name:</b> {{ schemaStore.schema.name }}</p>
        <p> <b>Version:</b> {{ schemaStore.schema.version }}</p>
        <p v-if="schemaStore.schema.description"> <b>Description:</b> {{ schemaStore.schema.description }}</p>
        <va-divider />
        <va-tabs grow v-model="tab">
            <template #tabs>
                <va-tab v-for="t in ['Sample', 'Experiment']" :key="t" :name="t">
                    {{ t }}
                </va-tab>
            </template>
        </va-tabs>
        <va-card>
            <va-data-table>
                
            </va-data-table>
        </va-card>
        <div class="row justify-center">
            <div class="flex">
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
import { ref, watchEffect } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import { useRouter } from 'vue-router';
import ProjectService from '../../services/clients/ProjectService';

const schemaStore = useSchemaStore()
const router = useRouter()
const props = defineProps<{
    id: string
}>()

const tab = ref('Sample')

watchEffect(async () => {
    const { data } = await ProjectService.getProject(props.id)
    schemaStore.schema = { ...data }
})

</script>