<template>
    <VaModal v-model="modelStore.showDeleteConfirmation" close-button hide-default-actions>
        <template #header>
            <h3 class="va-h3">
                Deleting {{ modelName }}
            </h3>
            <p class="va-text-secondary">Deleting the model is irreversible, the linked data will be also deleted</p>
        </template>
        <VaDivider />
        <div class="layout va-gutter-5">
            <div class="row align-center">
                <div class="flex lg12 md12 sm12 xs12">
                    <p class="va-text-danger">
                        This will permanently delete also the following data:
                    </p>
                </div>
                <div v-if="totalRecords" class="flex">
                    Records: <VaChip flat size="large">
                        {{ totalRecords }}
                    </VaChip>
                </div>
                <div v-if="totalProtocols" class="flex">
                    Protocols: <VaChip flat size="large">
                        {{ totalProtocols }}
                    </VaChip>
                </div>
                <div v-if="totalImages" class="flex">
                    Images: <VaChip flat size="large">
                        {{ totalImages }}
                    </VaChip>
                </div>
            </div>
            <div v-if="refModels.length > 0" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <p class="va-text-danger">
                        This will also delete the following related models:
                    </p>
                </div>
                <div v-for="refModel in refModels" :key="refModel.name" class="flex">
                    <VaChip>
                        {{ refModel.name }}
                    </VaChip>
                </div>
            </div>
        </div>
        <template #footer>
            <div class="row justify-space-between">
                <div class="flex">
                    <VaButton @click="modelStore.showDeleteConfirmation = !modelStore.showDeleteConfirmation"
                        color="textPrimary" preset="primary">Close</VaButton>
                </div>
                <div class="flex">
                    <VaButton :loading="loading" @click="deleteModel" color="danger">
                        Confirm Delete </VaButton>
                </div>
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

const refModels = computed(() => projectStore.models.filter(({ reference_model }) => reference_model === props.modelName))

const totalRecords = computed(() => modelStore.records)
const totalProtocols = computed(() => modelStore.protocols)
const totalImages = computed(() => modelStore.images)

async function deleteModel() {
    try {
        loading.value = true
        const { data } = await AuthService.deleteModel(props.projectId, props.modelName)
        init({ message: `Model ${props.modelName} and its related models ${refModels.value} have been deleted` })
    } catch (err) {
        const axiosError = err as AxiosError
        const responseData = axiosError.response?.data as { message: string }
        init({ message: responseData.message, color: 'danger' })
    } finally {
        loading.value = false
        modelStore.showDeleteConfirmation = !modelStore.showDeleteConfirmation
        router.push({ name: 'project', params: { projectId: props.projectId } })
    }
}

</script>