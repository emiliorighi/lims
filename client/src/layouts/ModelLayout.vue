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
                        <VaButton :disabled="isArchived" preset="primary" icon="fa-edit"></VaButton>
                    </div>
                    <div class="flex">
                        <VaButton @click="modelStore.showDeleteConfirmation = !modelStore.showDeleteConfirmation"
                            :disabled="isArchived" color="danger" preset="primary" icon="fa-trash"></VaButton>
                    </div>
                </div>
            </div>
        </div>
        <VaTabs color="textPrimary" v-model="viewValue">
            <template #tabs>
                <VaTab v-for="opt in options" :key="opt.value" :name="opt.value" :icon="opt.icon">
                    {{ opt.label }}
                </VaTab>
            </template>
        </VaTabs>
        <VaDivider style="margin-top: 0;" />
        <router-view></router-view>
        <ModelDeleteModal :project-id="projectId" :model-name="modelName" />
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useModelStore } from '../stores/model-store';
import { useProjectStore } from '../stores/project-store';
import { useRoute, useRouter } from 'vue-router';
import ModelDeleteModal from '../components/modals/ModelDeleteModal.vue';

type ViewType = 'details' | 'records' | 'links' | 'protocols' | 'images'
type Opt = { label: string, value: ViewType, icon: string }

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

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

watch(() => props.modelName, async () => {
    modelStore.setModel(models.value, props.modelName)
    await modelStore.getStats(props.projectId, props.modelName)
    currentView.value = 'records'
}, { immediate: true })

const options = computed(() => {
    const opts: Opt[] = []
    opts.push({ icon: 'fa-book-open', label: 'Details', value: 'details' })
    opts.push({ icon: 'fa-file-lines', label: `Records (${totalRecords.value})`, value: 'records' })
    opts.push({ icon: 'fa-scroll', label: `Protocols (${totalProtocols.value})`, value: 'protocols' })
    opts.push({ icon: 'fa-image', label: `Images (${totalImages.value})`, value: 'images' })

    return opts
})


</script>