<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <h3 class="va-h6">
                Project Information
            </h3>
            <VaCard outlined squared color="backgroundElement">
                <VaCardContent>
                    <p> <strong>Name: </strong><span>{{ project.name }}</span></p>
                    <p><strong>Version: </strong><span>{{ project.version }}</span></p>
                    <p v-if="project.description"><strong>Description: </strong><span>{{ project.description }}</span>
                    </p>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <ModelOverview v-for="refModel, idx in project.models" :key="refModel.name" :model="refModel"
        :title="refModel.name" />
</template>

<script setup lang="ts">
import ModelOverview from '../model/ModelDetails.vue'
import { ReseachProject } from '../../data/types';

const props = defineProps<{
    project:ReseachProject
}>()

</script>
