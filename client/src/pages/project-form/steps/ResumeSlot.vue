<template>
    <h4 class="va-h4"> Resume of {{ projectStore.currentProject.project_id }}
    </h4>
    <p class="va-text-secondary">Check the project and submit it</p>
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <ProjectOverviewCard :metadata="projectStore.currentProject" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../../stores/project-store'
import ProjectOverviewCard from '../../../components/cards/ProjectOverviewCard.vue';

const projectStore = useProjectStore()

</script>