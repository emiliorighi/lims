<template>
    <VaModal fullscreen hide-default-actions close-button v-model="modelStore.showForm">
        <template #header>
            <h3 class="va-h3">
                Model Form
            </h3>
        </template>
        <div class="layout fluid va-gutter-5">
            <VaForm ref="form">
                <div v-if="duplicatedName" class="row">
                    <div class="flex lg12 md12 sm12 xs12">
                        <p class="va-text-danger">This
                            name already exists,
                            change it</p>
                    </div>
                </div>
                <ModelInfo :description="modelForm.description" :type="modelForm.name"
                    @update-type="(v: string) => modelForm.name = v"
                    @update-description="(v: string) => modelForm.description = v" />
                <ModelReference v-if="existingModels.length" :models="existingModels"
                    :reference-model="modelForm.reference_model" :rules="[
                        (v: string) => !v || (v && existingModels.includes(v)) || 'Reference model is not present'
                    ]" @change="(v: string | undefined) => modelForm.reference_model = v">
                </ModelReference>
                <div v-if="modelForm.reference_model" class="row">
                    <div class="flex">
                        <VaCheckbox v-model="modelForm.inherit_reference_id"
                            :label="`Inherit identifier from ${modelForm.reference_model}, this will add the identifier of ${modelForm.reference_model} at the beginning of the ${modelForm.name} identifier `" />
                    </div>
                </div>
                <ModelAttributes v-model:model-attributes="modelForm.fields" />
                <ModelIdentifier :ref-model="modelForm.reference_model" :attributes="attributes"
                    @change="(v) => modelForm.id_format = v" :model-id="modelForm.id_format" />
                <VaInput style="visibility: hidden;" :rules="[(v: any) => !duplicatedName || 'Error']">
                </VaInput>
            </VaForm>
        </div>
        <template #footer>
            <div class="row justify-end">
                <div class="flex">
                    <VaButton @click="submit">Submit</VaButton>
                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useToast, useForm } from 'vuestic-ui/web-components';
import { ResearchModel } from '../../data/types';
import { useModelStore } from '../../stores/model-store';
import ModelInfo from '../forms/ModelInfo.vue';
import ModelAttributes from '../forms/ModelAttributes.vue';
import ModelIdentifier from '../forms/ModelIdentifier.vue';
import ModelReference from '../forms/ModelReference.vue';

const props = defineProps<{
    incomingModel?: ResearchModel
    existingModels: string[]
}>()

const emits = defineEmits(['submit'])
const { init } = useToast()
const { validate } = useForm('form')
const modelStore = useModelStore()
const initForm: ResearchModel = {
    name: '',
    description: '',
    fields: [],
    id_format: []
}
const modelForm = ref<ResearchModel>({ ...initForm })

const duplicatedName = computed(() => props.existingModels.includes(modelForm.value.name))
const attributes = computed(() => modelForm.value.fields.map(({ key }) => key))

watch(() => props.incomingModel, () => {
    if (props.incomingModel) modelForm.value = { ...props.incomingModel }
    else modelForm.value = { ...initForm }
}, { immediate: true })

function submit() {
    if (!validate()) {
        init({ message: 'Fill the required fields', color: 'danger' })
        return
    }
    emits('submit', modelForm.value)
    //resetForm
    modelForm.value = { ...initForm }
    modelStore.showForm = false
}
</script>