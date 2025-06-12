<template>
    <VaCard>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h2 class="va-h3">
                        Information
                    </h2>
                    <p class="va-text-secondary">Enter basic information about your model.</p>
                </div>
            </div>
            <div v-if="isControlledMode" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard
                        message="You are in controlled edit mode. Reference model and inheritance settings are disabled to prevent breaking existing dependencies."
                        icon="fa-warning" color="warning" />
                </div>
            </div>
            <div v-if="isControlledMode && isNameModified" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <AlertCard
                        message="Changing the model name will automatically update all models that reference this model. Please ensure this is intended."
                        icon="fa-warning" color="danger" />
                </div>
            </div>
            <div class="row">
                <div class="flex lg6 md6 sm12 xs12">
                    <VaInput required-mark v-model="modelData.name" :rules="[
                        (v: string) => v.length >= 3 || 'name is mandatory, at least 3 characters',
                        (v: string) => isEditMode || !existingModelsNames.includes(v) || 'This model name already exists'
                    ]" label="Name" placeholder="Type here your model name (example: Sample)"
                        :messages="['The name of your model (like sample, experiment etc.)']">
                    </VaInput>
                </div>
                <div class="flex lg6 md6 sm12 xs12">
                    <VaInput v-model="modelData.description" label="Description"
                        placeholder="Type a description for your model">
                    </VaInput>
                </div>
                <div v-if="existingModels.length" class="flex lg12 md12 sm12 xs12">
                    <VaSelect placeholder="Choose the model source referenced in this model" label="reference model"
                        v-model="modelData.reference_model" clearable :disabled="isControlledMode"
                        :options="existingModelsNames" :rules="[
                            (v: any) => !v || (v && existingModelsNames.includes(v)) || 'Reference model is not present'
                        ]">
                    </VaSelect>
                </div>
            </div>
            <div v-if="selectedRefModel" class="row">
                <div class="flex">
                    <VaCheckbox v-model="modelData.inherit_reference_id" :disabled="isControlledMode"
                        :label="`Inherit ${selectedRefModel.id_format.join('_')} at the beginning of the ${modelData.name} records identifiers.`" />
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ResearchModel, EditMode } from '../../../data/types'
import AlertCard from '../../cards/AlertCard.vue'

const props = defineProps<{
    modelValue: ResearchModel
    existingModels: ResearchModel[]
    mode: EditMode | 'create' | 'clone'
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: ResearchModel): void
}>()

const originalName = ref('')
const isNameModified = ref(false)

// Initialize or update the original name when either mode or modelValue changes
watch([() => props.mode, () => props.modelValue], ([newMode, newModel], [oldMode, oldModel]) => {
    // Only update if we have valid model data
    if (newModel && typeof newModel === 'object' && 'name' in newModel) {
        originalName.value = newModel.name
        isNameModified.value = false
    }
}, { immediate: true, deep: true })

watch(() => props.modelValue?.name, (newVal, oldVal) => {
    if (props.mode === 'edit-controlled' && oldVal && originalName.value) {
        isNameModified.value = newVal !== originalName.value
    }
})

const modelData = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const isControlledMode = computed(() => props.mode === 'edit-controlled')
const isEditMode = computed(() => props.mode.startsWith('edit-'))
const existingModelsNames = computed(() => props.existingModels.map(({ name }) => name))
const selectedRefModel = computed(() => props.existingModels.find(m => m.name === modelData.value.reference_model))
</script>