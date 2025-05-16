<template>
    <div>
        <div class="row align-center">
            <div class="flex">
                <h1 class="va-h1 va-text-capitalize">{{ modelName }}</h1>
                <p class="va-text-secondary">
                    {{ model?.description ? model.description : 'No description available' }}
                </p>
            </div>
            <div class="flex">
                <div class="row">
                    <div class="flex">
                        <VaDropdown
                            placement="bottom-start"
                            v-model="showEditDropdown"
                            stick-to-edges
                            :disabled="isArchived"
                        >
                        <template #anchor>
                            <VaButton :disabled="isArchived" preset="primary" icon="fa-edit">
                                Edit
                            </VaButton>
                        </template>

                        <VaCard class="ma-0">
                            <VaCardContent class="pa-0">
                                <div class="pa-2" style="min-width: 300px;">
                                    <template v-if="totalRecords > 0">
                                        <div 
                                            class="pa-2 cursor-pointer hover-bg" 
                                            @click="handleEditWithMode('edit-controlled')"
                                        >
                                            <h6 class="va-h6 mb-1">Controlled Mode</h6>
                                            <p class="va-text-secondary mb-0">Safe mode that prevents breaking changes to existing records and dependencies.</p>
                                        </div>
                                        <VaDivider />
                                        <div 
                                            class="pa-2 cursor-pointer hover-bg" 
                                            @click="handleEditWithMode('edit-override')"
                                        >
                                            <h6 class="va-h6 mb-1">Override Mode</h6>
                                            <p class="va-text-secondary mb-0">Advanced mode that allows all changes but may break existing records and dependencies.</p>
                                        </div>
                                    </template>
                                    <template v-else>
                                        <div 
                                            class="pa-2 cursor-pointer hover-bg" 
                                            @click="handleEditWithMode('edit-override')"
                                        >
                                            <h6 class="va-h6 mb-1">Edit Model</h6>
                                            <p class="va-text-secondary mb-0">Make changes to your model structure.</p>
                                        </div>
                                    </template>
                                    <VaDivider />
                                    <div 
                                        class="pa-2 cursor-pointer hover-bg" 
                                        @click="handleClone"
                                    >
                                        <h6 class="va-h6 mb-1">Clone Model</h6>
                                        <p class="va-text-secondary mb-0">Create a copy of this model with all its attributes and settings.</p>
                                    </div>
                                </div>
                            </VaCardContent>
                        </VaCard>
                        </VaDropdown>
                    </div>
                    <div class="flex">
                        <VaButton @click="modelStore.showDeleteConfirmation = !modelStore.showDeleteConfirmation"
                            :disabled="isArchived" color="danger" preset="primary" icon="fa-trash">Delete</VaButton>
                    </div>
                </div>
            </div>
        </div>
        <VaTabs color="textPrimary" class="va-text-capitalize" v-model="viewValue">
            <template #tabs>
                <VaTab v-for="opt in options" :key="opt.value" :name="opt.value">
                    {{ opt.value }} <VaChip v-if="opt.count" style="margin-left: 3px;" size="small"
                        color="backgroundElement">
                        {{ opt.count }}
                    </VaChip>
                </VaTab>
            </template>
        </VaTabs>
        <VaDivider style="margin-top: 0;" />
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <router-view></router-view>
            </div>
        </div>
        <ModelDeleteModal :project-id="projectId" :model-name="modelName" />
        <ModelFormModal 
            v-model="modelStore.showEditModal"
            :mode="editMode"
            :incoming-model="model || undefined"
            :existing-models="models"
            :project-id="projectId"
            :is-project-form="false"
            @submit="handleEditSubmit"
        />
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useModelStore } from '../stores/model-store';
import { useProjectStore } from '../stores/project-store';
import { useToast } from 'vuestic-ui';
import { ResearchModel, EditMode } from '../data/types';
import AuthService from '../services/clients/AuthService';
import { catchError } from '../composables/toastMessages';
import { useRoute, useRouter } from 'vue-router';
import ModelDeleteModal from '../components/modals/ModelDeleteModal.vue';
import ModelFormModal from '../components/modals/ModelFormModal.vue';

type ViewType = 'details' | 'records' | 'links' | 'protocols' | 'images'
type Opt = { value: ViewType, count?: number }

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

const editMode = ref<EditMode>('edit-controlled')
const { init } = useToast()

const currentView = ref<ViewType>('records')
const route = useRoute()
const router = useRouter()
const viewValue = computed(({
    get() {
        return route.name?.toString()
    },
    set(v: ViewType) {
        router.push({ name: v })
    }
}))
const modelStore = useModelStore()
const projectStore = useProjectStore()
const isArchived = computed(() => projectStore.isArchived)
const models = computed(() => projectStore.models)
const totalRecords = computed(() => modelStore.records)
const totalProtocols = computed(() => modelStore.protocols)
const totalImages = computed(() => modelStore.images)
const model = computed(() => modelStore.currentModel)

const showEditDropdown = ref(false)

watch(() => props.modelName, async () => {
    modelStore.setModel(models.value, props.modelName)
    await modelStore.getStats(props.projectId, props.modelName)
    currentView.value = 'records'
}, { immediate: true })

function handleEditWithMode(mode: EditMode) {
    editMode.value = mode
    showEditDropdown.value = false
    modelStore.toggleEditModal()
}

function handleClone() {
    editMode.value = 'clone' as EditMode
    showEditDropdown.value = false
    modelStore.toggleEditModal()
}

async function handleEditSubmit(updatedModel: ResearchModel) {
    try {
        if (modelStore.showEditModal && editMode.value.startsWith('edit-')) {
            // Update existing model
            const response = await AuthService.updateModel(props.projectId, props.modelName, updatedModel)
            init({ color: 'success', message: `${updatedModel.name} updated successfully` })
            
            // Refresh project data
            await projectStore.getProjectSchema(props.projectId)
            
            // Close the modal
            modelStore.showEditModal = false
            
            // If the model name was changed, redirect to the details page of the updated model
            if (updatedModel.name !== props.modelName) {
                router.push({
                    name: 'details',
                    params: { 
                        projectId: props.projectId,
                        modelName: updatedModel.name
                    }
                })
            }
        } else {
            // Create new model (clone case)
            const response = await AuthService.createModel(props.projectId, updatedModel)
            init({ color: 'success', message: `${updatedModel.name} created successfully` })
            
            // Refresh project data
            await projectStore.getProjectSchema(props.projectId)
            
            // Close the modal
            modelStore.showEditModal = false
            
            // Redirect to the details page of the newly created model
            router.push({
                name: 'details',
                params: { 
                    projectId: props.projectId,
                    modelName: updatedModel.name
                }
            })
        }
    } catch (error) {
        catchError(error)
    }
}

const options = computed(() => {
    const opts: Opt[] = []
    opts.push({ value: 'details' })
    opts.push({ count: totalRecords.value, value: 'records' })
    opts.push({ count: totalProtocols.value, value: 'protocols' })
    opts.push({ count: totalImages.value, value: 'images' })
    return opts
})

</script>

<style scoped>
.hover-bg {
    border-radius: var(--va-border-radius);
}
.hover-bg:hover {
    background-color: var(--va-background-element);
}
.cursor-pointer {
    cursor: pointer;
}
</style>