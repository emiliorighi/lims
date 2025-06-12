<template>
    <VaCard>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h2 class="va-h3">Models</h2>
                    <p class="va-text-secondary">
                        A model can be considered as a TSV file. Add as many models
                        as
                        TSV
                        files you
                        have, or use the same TSV
                        file to split your entries in more models. In case your TSV
                        files
                        reference
                        each other, fill the
                        reference model field with the name of the target model.
                    </p>
                </div>
            </div>
            <div v-if="!modelNames.length" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard message="Add at least one model" icon="fa-warning" color="danger" />
                </div>
            </div>
            <div class="row">
                <div v-for="model, idx in models" :key="model.name" class="flex lg12 md12 sm12 xs12">
                    <VaCard color="backgroundElement">
                        <VaCardContent>
                            <div class="row align-center">
                                <div class="flex">
                                    <div class="row align-center">
                                        <div class="flex">
                                            <h3 class="va-h6">
                                                {{ model.name }}
                                            </h3>
                                            <p class="va-text-secondary">{{
                                                model.description }}</p>
                                        </div>
                                        <div v-if="model.reference_model" class="flex">
                                            <VaChip color="backgroundElement" size="small" icon="fa-link">{{
                                                model.reference_model }}</VaChip>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex">
                                    <div class="row">
                                        <div class="flex">
                                            <VaButton @click="editModel(model)" preset="primary" icon="fa-edit">
                                            </VaButton>
                                        </div>
                                        <div class="flex">
                                            <VaButton @click="projectStore.deleteModel(idx)" color="danger"
                                                preset="primary" icon="fa-trash">
                                            </VaButton>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>
            <div class="row align-center">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaButton @click="addModel" icon="fa-plus" size="large">
                        Add model
                    </VaButton>
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../stores/project-store'
import { computed } from 'vue';
import { ResearchModel } from '../../data/types';
import AlertCard from '../../components/cards/AlertCard.vue';

const projectStore = useProjectStore()

const models = computed(() => projectStore.projectForm.models)
const modelNames = computed(() => models.value.map(({ name }) => name))


function addModel() {
    projectStore.selectedModel = undefined
    projectStore.showModelForm = true
}

function editModel(model: ResearchModel) {
    projectStore.selectedModel = { ...model }
    projectStore.showModelForm = true
}


</script>
