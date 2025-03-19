<template>
    <div class="row">
        <div class="flex">
            <p class="va-text-secondary">
                A model can be considered as a TSV file. Add as many models as TSV files you have, or use the same TSV
                file to split your entries in more models. In case your TSV files reference each other, fill the
                reference model field with the name of the target model.
            </p>
        </div>
    </div>
    <div class="row">
        <div class="flex">
            <VaButton @click="addRefModel" color="textPrimary">Add New Model</VaButton>
        </div>
    </div>
    <div v-for="refModel, idx in projectStore.projectForm.models" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard :stripe="duplicates.includes(refModel.name)"
                :stripe-color="duplicates.includes(refModel.name) ? 'danger' : undefined">
                <VaCardContent>
                    <div class="row justify-space-between">
                        <div class="flex">
                            <h2 class="va-h6">
                                Model {{ idx + 1 }}
                            </h2>
                        </div>
                        <div class="flex">
                            <VaButton @click="deleteRefModel(idx)" color="danger">Delete</VaButton>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <p v-if="duplicates.includes(refModel.name)" class="va-text-danger">This name already exists,
                        change it</p>
                    <ModelInfo :description="refModel.description" :type="refModel.name"
                        @update-type="(v: string) => refModel.name = v"
                        @update-description="(v: string) => refModel.description = v" />
                    <Attributes v-model:model-attributes="refModel.fields" />
                    <ModelIdentifier :attributes="refModel.fields.map(({ key }) => key)"
                        @change="(v) => refModel.id_format = v" :model-id="refModel.id_format" />
                    <ModelReference v-if="refModelNames.length > 1" :models="refModelNames"
                        :reference-model="refModel.reference_model" :rules="[
                            (v: string) => !v || (v && refModelNames.includes(v)) || 'Reference model is not present'
                        ]" @change="(v: string | undefined) => refModel.reference_model = v">

                    </ModelReference>
                    <!-- <div v-if="refModelNames.length > 1" class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaSelect label="The reference model name" v-model="refModel.reference_model"
                                :options="refModelNames.filter(name => name !== refModel.name)" clearable :rules="[
                                    (v: string) => !v || (v && refModelNames.includes(v)) || 'Reference model is not present'
                                ]">
                            </VaSelect>
                        </div>
                    </div> -->
                    <VaInput style="visibility: hidden;" :rules="[duplicates.length === 0]"></VaInput>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useProjectStore } from '../../../stores/project-store';
import { computed, ref } from 'vue'
import ModelIdentifier from '../../../components/model/ModelIdentifier.vue';
import Attributes from '../../../components/model/ModelAttributes.vue';
import ModelInfo from '../../../components/model/ModelInfo.vue';
import ModelReference from '../../../components/model/ModelReference.vue';

const projectStore = useProjectStore()

const refModels = computed(() => projectStore.projectForm.models)

const refModelNames = computed(() => refModels.value.map(({ name }) => name))
const duplicates = computed(() => findDuplicates(refModels.value, 'name'))


function addRefModel() {
    projectStore.projectForm.models.push(
        {
            name: '',
            description: '',
            protocols: [],
            links: [],
            fields: [],
            id_format: []
        }
    )
}

function deleteRefModel(index: number) {
    projectStore.projectForm.models = [...projectStore.projectForm.models.slice(0, index), ...projectStore.projectForm.models.slice(index + 1)]

}

function findDuplicates<T, K extends keyof T>(items: T[], key: K): T[K][] {
    const counts = new Map<T[K], number>();

    // Count the occurrences of each value
    items.forEach(item => {
        const value = item[key];
        counts.set(value, (counts.get(value) || 0) + 1);
    });

    // Return values that appear more than once
    const duplicates: T[K][] = [];
    counts.forEach((count, value) => {
        if (count > 1) {
            duplicates.push(value);
        }
    });

    return duplicates;
}
</script>