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
                        <VaButton @click="modelStore.showDeleteConfirmation = !modelStore.showDeleteConfirmation"
                            :disabled="isArchived" color="danger" preset="primary" icon="fa-trash"></VaButton>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="flex">
                <VaButtonGroup>
                    <VaButton class="va-text-capitalize" :preset="viewValue === opt.value ? undefined : 'primary'"
                        @click="viewValue = opt.value" color="textPrimary" v-for="opt in options" :key="opt.value">
                        {{ opt.value }}
                        <template v-if="opt.count !== undefined" #append>
                            <VaChip style="margin-left: 3px;" size="small" color="backgroundElement">
                                {{ opt.count }}
                            </VaChip>
                        </template>
                    </VaButton>
                </VaButtonGroup>
            </div>
        </div>
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
type Opt = { value: ViewType, count?: number }

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
    opts.push({ value: 'details' })
    opts.push({ count: totalRecords.value, value: 'records' })
    opts.push({ count: totalProtocols.value, value: 'protocols' })
    opts.push({ count: totalImages.value, value: 'images' })
    return opts
})


</script>