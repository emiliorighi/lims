<template>
    <VaModal v-model="modelStore.showDeleteConfirmation" close-button hide-default-actions size="small">
        <template #header>
            <h3 class="va-h3 mb-1">Delete Model: {{ modelName }}</h3>
            <VaDivider />
        </template>

        <div class="pa-4">
            <!-- Warning Message -->
            <div class="mb-4">
                <p class="va-text-danger mb-2">
                    <i class="fa fa-exclamation-triangle mr-2"></i>
                    <strong>Warning: This action cannot be undone</strong>
                </p>
                <p class="va-text-secondary">
                    This will permanently delete the model and all associated data.
                </p>
            </div>

            <!-- Primary Data Section -->
            <div v-if="hasAssociatedData" class="mb-4">
                <h5 class="va-h5 mb-2">Associated Data to be Deleted:</h5>
                <div class="data-grid">
                    <div v-if="totalRecords" class="data-item">
                        <i class="fa fa-database mr-2"></i>
                        <span>{{ totalRecords }} Records</span>
                    </div>
                    <div v-if="totalProtocols" class="data-item">
                        <i class="fa fa-file-text mr-2"></i>
                        <span>{{ totalProtocols }} Protocols</span>
                    </div>
                    <div v-if="totalImages" class="data-item">
                        <i class="fa fa-image mr-2"></i>
                        <span>{{ totalImages }} Images</span>
                    </div>
                </div>
            </div>

            <!-- Related Models Section -->
            <div v-if="refModels.length > 0" class="mb-4">
                <h5 class="va-h5 mb-2">Dependent Models to be Deleted:</h5>
                <p class="va-text-secondary mb-2">
                    The following models reference {{ modelName }} and will also be deleted:
                </p>
                <div class="dependent-models">
                    <VaChip 
                        v-for="refModel in refModels" 
                        :key="refModel.name"
                        class="mr-2 mb-2"
                        color="danger"
                        size="small"
                    >
                        {{ refModel.name }}
                    </VaChip>
                </div>
            </div>

            <!-- Confirmation Input -->
            <div class="confirmation-section">
                <p class="mb-2">Type <strong>{{ modelName }}</strong> to confirm deletion:</p>
                <VaInput
                    v-model="confirmationText"
                    :success="isConfirmed"
                    :error="showError"
                    class="mb-2"
                />
            </div>
        </div>

        <template #footer>
            <VaDivider class="mt-0" />
            <div class="row justify-space-between pa-4">
                <VaButton
                    @click="modelStore.showDeleteConfirmation = false"
                    color="secondary"
                    outline
                >
                    Cancel
                </VaButton>
                <VaButton
                    :loading="loading"
                    @click="deleteModel"
                    :disabled="!isConfirmed"
                    color="danger"
                >
                    Delete Model
                </VaButton>
            </div>
        </template>
    </VaModal>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import AuthService from '../../services/clients/AuthService';
import { AxiosError } from 'axios';
import { useToast } from 'vuestic-ui/web-components';
import { useModelStore } from '../../stores/model-store';
import { useProjectStore } from '../../stores/project-store';
import { useRouter } from 'vue-router';

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

const { init } = useToast()
const modelStore = useModelStore()
const projectStore = useProjectStore()
const router = useRouter()

const loading = ref(false)
const confirmationText = ref('')

const refModels = computed(() => projectStore.models.filter(({ reference_model }) => reference_model === props.modelName))
const totalRecords = computed(() => modelStore.records)
const totalProtocols = computed(() => modelStore.protocols)
const totalImages = computed(() => modelStore.images)

const hasAssociatedData = computed(() => totalRecords.value > 0 || totalProtocols.value > 0 || totalImages.value > 0)
const isConfirmed = computed(() => confirmationText.value === props.modelName)
const showError = computed(() => confirmationText.value !== '' && !isConfirmed.value)

async function deleteModel() {
    if (!isConfirmed.value) return

    try {
        loading.value = true
        await AuthService.deleteModel(props.projectId, props.modelName)
        
        const message = refModels.value.length > 0 
            ? `Model ${props.modelName} and its ${refModels.value.length} dependent models have been deleted`
            : `Model ${props.modelName} has been deleted`
            
        init({ message, color: 'success' })
        
        // Refresh project schema to update sidebar
        await projectStore.getProjectSchema(props.projectId)
        
        modelStore.showDeleteConfirmation = false
        router.push({ name: 'project', params: { projectId: props.projectId } })
    } catch (err) {
        const axiosError = err as AxiosError
        const responseData = axiosError.response?.data as { message: string }
        init({ message: responseData.message, color: 'danger' })
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.data-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
}

.data-item {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    background-color: var(--va-background-element);
    border-radius: var(--va-border-radius);
}

.dependent-models {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.confirmation-section {
    background-color: var(--va-background-element);
    padding: 1rem;
    border-radius: var(--va-border-radius);
    margin-top: 1rem;
}
</style>