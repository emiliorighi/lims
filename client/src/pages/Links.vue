<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <div class="row align-center justify-space-between">
                <div class="flex lg4 md6">
                    <VaInput v-model="linkStore.filter" background="backgroundSecondary" @update:model-value="debouncedSearch"
                        :placeholder="`Search ${type}...`" clearable class="w-full">
                        <template #prependInner>
                            <VaIcon name="fa-search" color="textPrimary" />
                        </template>
                    </VaInput>
                </div>
                <div class="flex">
                    <VaButton class="mr-2" preset="secondary" color="textPrimary" icon="fa-download"
                        :disabled="!linkStore.links.length || loading" :loading="downloading" @click="downloadAllFiles">
                        Download {{ type }}
                    </VaButton>
                    <VaButton v-if="role === 'admin' || role === 'project_manager' || role === 'data_manager'" preset="secondary" color="textPrimary" icon="fa-file-upload" :disabled="isArchived"
                        :to="{ name: 'link-upload', params: { projectId: projectId, modelName: modelName, type: type } }">
                        Upload {{ type }}
                    </VaButton>
                </div>
            </div>
            <div class="row row-equal justify-center">
                <!-- Empty State -->
                <div v-if="!linkStore.links.length && !linkStore.filter" class="flex lg12 md12 sm12 xs12">
                    <VaCard class="empty-state-card">
                        <VaCardContent>
                            <div class="column align-center text-center">
                                <VaIcon :name="type === 'images' ? 'fa-image' : 'fa-scroll'" size="large"
                                    color="neutral" class="mb-4" />
                                <h3 class="va-h3 mb-2">No {{ type }} yet</h3>
                                <p v-if="role === 'admin' || role === 'project_manager' || role === 'data_manager'" class="va-text-secondary mb-4">
                                    {{ type === 'images' ?
                                        'Start adding images to your model to visualize your data.' :
                                        'Add protocols to document your research methods and procedures.'
                                    }}
                                </p>
                                <VaButton v-if="role === 'admin' || role === 'project_manager' || role === 'data_manager'" preset="secondary" color="textPrimary" icon="fa-file-upload"
                                    :disabled="isArchived"
                                    :to="{ name: 'link-upload', params: { projectId: projectId, modelName: modelName, type: type } }">
                                    Upload your first {{ type === 'images' ? 'image' : 'protocol' }}
                                </VaButton>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
                <!-- No Results from Search -->
                <div v-else-if="!linkStore.links.length && linkStore.filter" class="flex lg12 md12 sm12 xs12">
                    <VaCard >
                        <VaCardContent>
                            <div class="column align-center text-center">
                                <VaIcon name="fa-search" size="large" color="neutral" class="mb-2" />
                                <h3 class="va-h3 mb-2">No results found</h3>
                                <p class="va-text-secondary mb-4">
                                    No {{ type }} match your search "{{ linkStore.filter }}". Try adjusting your search
                                    terms.
                                </p>
                                <VaButton color="textPrimary" preset="plain" @click="clearSearch">
                                    Clear search
                                </VaButton>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
                <!-- Links List -->
                <template v-else>
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaInfiniteScroll :loading="loading" :load="handleLoadMore" class="row row-equal">
                            <div v-for="link in linkStore.links" :key="link.name" class="flex lg4 md6 sm12 xs12">
                                <LinkDetailsCard @show="handleShow" @delete="triggerDelete" :link="link" :type="type" />

                            </div>
                            <template #loading>
                                <div class="flex justify-center my-4">
                                    <VaSpinner size="small" />
                                </div>
                            </template>
                        </VaInfiniteScroll>
                    </div>
                </template>
            </div>
        </div>
    </div>
    <VaModal v-model="showDeleteConfirmation" hide-default-actions>
        <template #header>
            <div class="row align-center justify-space-between">
                <div class="flex">
                    <h3 class="va-h3">
                        Deleting {{ protocolToDelete?.name }}
                    </h3>
                </div>
            </div>
        </template>
        <VaDivider />
        <div class="row align-center justify-space-between">
            <div class="flex">
                <p class="va-text-danger">
                    This will permanently delete the object
                </p>
            </div>
        </div>
        <template #footer>
            <div class="row justify-space-between">
                <div class="flex">
                    <VaButton @click="showDeleteConfirmation = false" color="textPrimary" preset="plain">
                        Cancel
                    </VaButton>
                </div>
                <div v-if="role === 'admin' || role === 'project_manager' || role === 'data_manager'" class="flex">
                    <VaButton @click="deleteImage" color="danger" :loading="deleting">
                        Delete
                    </VaButton>
                </div>
            </div>
        </template>
    </VaModal>
    <VaModal hide-default-actions close-button v-model="showImage" size="large">
        <div class="layout">
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VueFilesPreview :file="imageSrc" />
                </div>
            </div>
        </div>
    </VaModal>
    <LinkFormModal :model-name="modelName" :project-id="projectId" :type="type" />
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { debounce } from '../composables/debounce';
import { useModelStore } from '../stores/model-store';
import { LinkType } from '../data/types';
import { useProjectStore } from '../stores/project-store';
import { useLinkStore } from '../stores/link-store';
import LinkFormModal from '../components/modals/LinkFormModal.vue';
import LinkDetailsCard from '../components/cards/LinkDetailsCard.vue';
import { VueFilesPreview } from 'vue-files-preview';
import { catchError } from '../composables/toastMessages';
import { useGlobalStore } from '../stores/global-store';

const gStore = useGlobalStore()
const role = computed(() => gStore.user.role)

const props = defineProps<{
    projectId: string,
    modelName: string,
    type: LinkType,
}>()

const linkStore = useLinkStore()
const modelStore = useModelStore()
const projectStore = useProjectStore()
const showDeleteConfirmation = ref(false)
const showImage = ref(false)
const imageSrc = ref<File | undefined>(undefined)
const extension = ref('')
const protocolToDelete = ref<Record<string, any> | null>(null)
const loading = ref(false)
const downloading = ref(false)
const deleting = ref(false)

const total = computed(() => linkStore.total)
const isArchived = computed(() => projectStore.isArchived)
const hasMore = computed(() => linkStore.links.length < total.value)

watch(() => [props.modelName, props.type], async () => {
    linkStore.filter = ""
    linkStore.resetPagination()
    await linkStore.fetchProjectModelLinks(props.projectId, props.modelName, props.type)
}, { immediate: true })

const debouncedSearch = debounce(async () => {
    await handleSearch()
}, 200);

async function handleSearch() {
    linkStore.resetPagination()
    await linkStore.fetchProjectModelLinks(props.projectId, props.modelName, props.type)
}

function clearSearch() {
    linkStore.filter = ""
    handleSearch()
}

async function handleLoadMore() {
    if (!hasMore.value || loading.value) return

    loading.value = true
    try {
        linkStore.pagination.offset += linkStore.pagination.limit
        await linkStore.fetchProjectModelLinks(props.projectId, props.modelName, props.type)
    } finally {
        loading.value = false
    }
}

async function handleShow(src: string, extension: string) {
    try {
        const response = await fetch(src)
        const blob = await response.blob()
        imageSrc.value = new File([blob], `file.${extension}`, { type: blob.type })
        showImage.value = !showImage.value
    } catch (error) {
        catchError(error)
    }
}

function triggerDelete(protocol: Record<string, any>) {
    protocolToDelete.value = { ...protocol }
    showDeleteConfirmation.value = !showDeleteConfirmation.value
}

async function deleteImage() {
    if (!protocolToDelete.value) return
    deleting.value = true
    try {
        await linkStore.deleteLink(props.projectId, props.modelName, protocolToDelete.value.name, props.type)
        showDeleteConfirmation.value = !showDeleteConfirmation.value
        await handleSearch()
        await modelStore.getStats(props.projectId, props.modelName)
    } finally {
        deleting.value = false
    }
}

async function downloadAllFiles() {
    downloading.value = true
    try {
        await linkStore.downloadFiles(props.projectId, props.modelName, props.type)
    } catch (error) {
        console.error('Error downloading files:', error)
    } finally {
        downloading.value = false
    }
}
</script>

<style scoped>
.mb-2 {
    margin-bottom: 0.5rem;
}

.mb-4 {
    margin-bottom: 1rem;
}

.mt-4 {
    margin-top: 1rem;
}

.mr-2 {
    margin-right: 0.5rem;
}

.text-center {
    text-align: center;
}

.column {
    display: flex;
    flex-direction: column;
}

.align-center {
    align-items: center;
}

.w-full {
    width: 100%;
}

</style>