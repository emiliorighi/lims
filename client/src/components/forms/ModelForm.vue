<template>
    <div class="row align-center justify-space-between">
        <div class="flex">
            <h1 class="va-h1">{{ modalTitle }}</h1>
        </div>
        <div class="flex">
            <VaButton color="textPrimary" preset="secondary" icon="fa-chevron-left" @click="closeForm">Go Back</VaButton>
        </div>
    </div>
    <div v-if="props.mode === 'edit-override' && (totalRecords > 0 || dependencies.length > 0)" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <EditOverrideCard :total-records="totalRecords" :dependencies="dependencies" :related-model-records-counts="relatedModelRecordsCounts" :project-id="projectId" :incoming-model="incomingModel" :existing-models="existingModels" />
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaForm ref="mForm">
                <VaStepper v-model="step" :steps="steps" linear @finish="submit">
                    <template #step-content-0>
                        <ModelFormInformation v-model="modelForm" :mode="mode"
                            :existing-models="existingModels" />
                    </template>
                    <template #step-content-1>
                        <ModelFormAttributes v-model="modelForm" :mode="mode" />
                    </template>
                    <template #step-content-2>
                        <ModelIdentifier :model-name="modelForm.name" v-if="modelForm.fields.length"
                            :refModelIdFields="sourceModel?.id_format" :ref-model="modelForm.reference_model"
                            :attributes="modelForm.fields.map(f => f.key)" :disabled="isControlledMode"
                            @change="(v) => modelForm.id_format = v" :model-id="modelForm.id_format" />
                    </template>
                    <template #step-content-3>
                        <ModelFormResume :model-value="modelForm" :source-model="sourceModel" />
                    </template>
                </VaStepper>
            </VaForm>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue';
import { useForm, defineVaStepperSteps, useToast } from 'vuestic-ui/web-components';
import { ResearchModel, EditMode } from '../../data/types';
import ModelFormInformation from './model/ModelFormInformation.vue';
import ModelFormAttributes from './model/ModelFormAttributes.vue';
import ModelFormResume from './model/ModelFormResume.vue';
import ModelIdentifier from './ModelIdentifier.vue'
import { useModelStore } from '../../stores/model-store';
import ModelService from '../../services/clients/ModelService';
import EditOverrideCard from '../cards/EditOverrideCard.vue';

const props = defineProps<{
    incomingModel?: ResearchModel
    existingModels: ResearchModel[]
    mode: EditMode | 'create' 
    projectId?: string
    totalRecords?: number
    fromProject?: boolean
}>()

const { init } = useToast()
const emits = defineEmits(['submit', 'close'])
const { validate } = useForm('mForm')

const initForm: ResearchModel = {
    name: '',
    description: '',
    fields: [],
    id_format: []
}

const step = ref(0)
const modelForm = ref<ResearchModel>({ ...initForm })
const modelStore = useModelStore()
const sourceModel = computed(() => props.existingModels.find(m => m.name === modelForm.value.reference_model))
const isControlledMode = computed(() => props.mode === 'edit-controlled')

onMounted(async () => {
    if (props.mode === 'edit-override') {
        loadDependencies()
    }
})

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
const modalTitle = computed(() => {
    if (props.fromProject) {
        return props.incomingModel ? 'Edit Model' : 'Add Model'
    }
    if (props.incomingModel) {
        if (props.mode === 'edit-controlled') {
            return 'Edit Model (Controlled)'
        } else if (props.mode === 'edit-override') {
            return 'Edit Model (Override)'
        }
    }

    return props.mode === 'clone' ? 'Clone Model' : 'Create Model'
})
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
        label: 'Attributes',
        beforeLeave: (step) => {
            step.hasError = !validate()
        }
    },
    {
        label: 'Identifier',
        beforeLeave: (step) => {
            step.hasError = !validate()
        }
    },
    {
        label: 'Resume',
    }
]))


async function submit() {
    if (validate()) {
        emits('submit', modelForm.value)
    }
}

function closeForm() {
    emits('close')
}


</script>