<template>
    <VaModal max-height="500px" size="large" v-model="projectStore.confirmOverwrite" hide-default-actions>
        <template #header>
            <Header :title="projectStore.incomingProject?.project_id"
                description="Choose if you want to overwrite or keep the current Form" />
        </template>

        <VaDivider />
        <VaCardBlock v-if="projectStore.incomingProject" horizontal>
            <VaCardBlock class="flex-auto">
                <VaButton color="secondary" @click="keep" icon-right="chevron_right"> Keep
                </VaButton>
                <ProjectOverviewCard :metadata="projectStore.currentProject" />
            </VaCardBlock>
            <VaDivider vertical />
            <VaCardBlock class="flex-auto">
                <VaButton color="warning" @click="overwrite" icon="chevron_left"> Overwrite
                </VaButton>
                <ProjectOverviewCard :metadata="projectStore.incomingProject" />
            </VaCardBlock>
        </VaCardBlock>
    </VaModal>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../stores/project-store'
import ProjectOverviewCard from '../../components/project/ProjectOverviewCard.vue';
import Header from './common/Header.vue'

const projectStore = useProjectStore()

function keep() {
    projectStore.switchConfirm()
}
function overwrite() {
    projectStore.overwriteProject()
    projectStore.switchConfirm()
}


</script>