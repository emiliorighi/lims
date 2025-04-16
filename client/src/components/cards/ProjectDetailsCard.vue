<template>
    <VaCard>
        <VaCardActions>
            <h2 class="va-h6">
                Project Information
            </h2>
        </VaCardActions>
        <VaCardContent>
            <p> <strong>Name: </strong><span>{{ project.name }}</span></p>
            <p><strong>Version: </strong><span>{{ project.version }}</span></p>
            <p v-if="project.description"><strong>Description: </strong><span>{{ project.description }}</span>
            </p>
        </VaCardContent>
        <VaCardActions>
            <h3 class="va-h6">
                Models:
            </h3>
        </VaCardActions>
        <VaCardContent v-for="model in models" :key="model.name">
            <ModelDetailsCard :model="model" :title="model.name" />
        </VaCardContent>
    </VaCard>
</template>

<script setup lang="ts">
import { ReseachProject } from '../../data/types';
import ModelDetailsCard from './ModelDetailsCard.vue';
import { computed } from 'vue';

const props = defineProps<{
    project: ReseachProject
}>()

const models = computed(() => props.project.models)

</script>
