<template>
    <VaModal fullscreen hide-default-actions close-button v-model="isVisible">
        <div class="layout va-gutter-5">
            <div class="row justify-center">
                <div class="flex lg12 md12 sm12 xs12">
                    <h1 class="va-h1">
                        {{ modalTitle }}
                    </h1>
                    <p v-if="!isEditMode && !isCloneMode" class="va-text-secondary">A model serves as a
                        structured container for your
                        data. It
                        allows you to define custom attributes that act as keys for the records it contains.
                        Additionally, you
                        can link this Model to existing models within the same project, enabling data relationships
                        and
                        references.

                        You also have the option to import data from a TSV file, where you can map the TSV columns
                        to the attributes defined in your Model, simplifying data entry and integration.</p>
                </div>
            </div>

            <!-- Warning Section -->
            <div v-if="props.mode === 'edit-override' && (totalRecords > 0 || dependencies.length > 0)" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard stripe stripe-color="danger">
                        <VaCardContent>
                            <div class="row align-center">
                                <div class="flex">
                                    <VaIcon name="fa-exclamation-triangle" color="danger" />
                                </div>
                                <div class="flex">
                                    <h2 class="va-h6">
                                        Warning: You are in override mode. Changes made in this mode can potentially break {{ totalRecords }} existing record{{ totalRecords !== 1 ? 's' : '' }}{{ dependencies.length ? ` and ${dependencies.length} dependent model${dependencies.length !== 1 ? 's' : ''}` : '' }}.
                                    </h2>
                                </div>
                            </div>
                            <div v-if="dependencies.length" class="row mt-2">
                                <div class="flex">
                                    <p class="va-text-secondary mb-2">
                                        Dependent models and their referencing records:
                                    </p>
                                </div>
                                <div v-for="dep in dependencies" :key="dep.key" class="flex lg12 md12 sm12 xs12">
                                    <RecordsDeleteCard :columns="dep.columns" :count="dep.value" :model-name="dep.key"
                                        :project-id="props.projectId || ''" />
                                </div>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
            </div>

            <VaForm ref="mForm">
                <VaStepper v-model="step" :steps="steps" linear @finish="submit">
                    <template #step-content-0>
                        <ModelFormInformation
                            v-model="modelForm"
                            :mode="props.mode"
                            :existing-models="existingModels"
                        />
                    </template>
                    <template #step-content-1>
                        <ModelFormAttributes
                            v-model="modelForm"
                            :mode="props.mode"
                            :existing-models="existingModels"
                            :has-records="totalRecords > 0"
                        />
                    </template>
                    <template #step-content-2>
                        <ModelFormResume
                            :model-value="modelForm"
                        />
                    </template>
                </VaStepper>
            </VaForm>
        </div>
    </VaModal>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useToast, useForm, defineVaStepperSteps } from 'vuestic-ui/web-components';
import { ResearchModel, EditMode } from '../../data/types';
import { useModelStore } from '../../stores/model-store';
import ModelService from '../../services/clients/ModelService';
import RecordsDeleteCard from '../cards/RecordsDeleteCard.vue';
import ModelFormInformation from '../forms/model/ModelFormInformation.vue';
import ModelFormAttributes from '../forms/model/ModelFormAttributes.vue';
import ModelFormResume from '../forms/model/ModelFormResume.vue';

const props = defineProps<{
    incomingModel?: ResearchModel
    existingModels: ResearchModel[]
    mode: EditMode | 'create' | 'clone'
    projectId?: string
    modelValue: boolean
}>()

const emits = defineEmits(['submit', 'update:modelValue'])
const { init } = useToast()
const { validate } = useForm('mForm')
const modelStore = useModelStore()

const initForm: ResearchModel = {
    name: '',
    description: '',
    fields: [],
    id_format: []
}

const step = ref(0)
const modelForm = ref<ResearchModel>({ ...initForm })

function createClonedModel(model: ResearchModel): ResearchModel {
    return {
        name: `${model.name}_copy`,
        description: model.description || '',
        fields: [...model.fields],
        id_format: [...model.id_format],
        reference_model: model.reference_model,
        inherit_reference_id: model.inherit_reference_id || false
    }
}

// Initialize form data when incoming model changes
watch([() => props.incomingModel, () => props.mode], ([newModel, newMode]) => {
    if (!newModel) {
        modelForm.value = { ...initForm }
        return
    }

    if (newMode === 'clone') {
        modelForm.value = createClonedModel(newModel)
    } else {
        modelForm.value = { ...newModel }
    }
}, { immediate: true, deep: true })

const steps = ref(defineVaStepperSteps([
    {
        label: 'Primary Information',
        beforeLeave: (step) => {
            step.hasError = !validate()
        }
    },
    {
        label: 'Attributes and Identifier',
        beforeLeave: (step) => {
            step.hasError = !validate()
        }
    },
    {
        label: 'Resume',
    }
]))

const isVisible = computed({
    get: () => props.modelValue,
    set: (value: boolean) => emits('update:modelValue', value)
})

// Handle modal visibility changes
watch(() => isVisible.value, async (newValue) => {
    if (!newValue) {
        // Reset form when closing if not in edit mode
        if (!isEditMode.value) {
            modelForm.value = { ...initForm }
        }
        step.value = 0
    } else if (isEditMode.value && !isCloneMode.value) {
        // Only load dependencies in edit modes (not clone)
        await loadDependencies()
    }
})

const isEditMode = computed(() => props.mode?.startsWith('edit-'))
const isCloneMode = computed(() => props.mode === 'clone')
const modalTitle = computed(() => {
    if (props.incomingModel) {
        if (props.mode === 'edit-controlled') {
            return 'Edit Model (Controlled)'
        } else if (props.mode === 'edit-override') {
            return 'Edit Model (Override)'
        }
    }
    
    return props.mode === 'clone' ? 'Clone Model' : 'Create Model'
})

// State for dependency tracking
const relatedModelRecordsCounts = ref<Record<string, number>>({})
const dependencies = computed(() => {
    return Object.entries(relatedModelRecordsCounts.value)
        .filter(([k, v]) => Boolean(v))
        .map(([k, v]) => {
            const columns = referencingModels.value.find(m => m.name === k)?.fields.map(({ key }) => key) ?? []
            return { key: k, value: v, columns }
        })
})

const referencingModels = computed(() => props.existingModels.filter(({ reference_model }) => reference_model === modelForm.value.name))
const totalRecords = computed(() => modelStore.records)

async function submit() {
    if (validate()) {
        emits('submit', modelForm.value)
        isVisible.value = false
    }
}

async function loadDependencies() {
    if (props.projectId && props.incomingModel) {
        try {
            const { data } = await ModelService.getRelatedModelsRecordCount(props.projectId, props.incomingModel.name)
            relatedModelRecordsCounts.value = { ...data }
        } catch (error) {
            console.error('Error loading dependencies:', error)
            init({ message: 'Error loading model dependencies', color: 'danger' })
        }
    }
}
</script>