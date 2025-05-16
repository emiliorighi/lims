<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <div class="row align-center justify-space-between mb-4">
                <div class="flex lg4 md6">
                    <VaInput v-model="linkStore.filter" @update:model-value="debouncedSearch"
                        :placeholder="`Search ${type}...`" clearable>
                    </VaInput>
                </div>
                <div class="flex">
                    <VaButton class="mr-2" icon="fa-download" :disabled="!linkStore.links.length"
                        @click="downloadAllFiles">
                        Download All
                    </VaButton>
                    <VaButton color="success" icon="fa-file-upload" :disabled="isArchived"
                        @click="linkStore.toggleModal">
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
                                <VaIcon 
                                    :name="type === 'images' ? 'fa-image' : 'fa-scroll'"
                                    size="large"
                                    color="neutral"
                                    class="mb-4"
                                />
                                <h3 class="va-h3 mb-2">No {{ type }} yet</h3>
                                <p class="va-text-secondary mb-4">
                                    {{ type === 'images' ? 
                                        'Start adding images to your model to visualize your data.' : 
                                        'Add protocols to document your research methods and procedures.' 
                                    }}
                                </p>
                                <VaButton
                                    color="primary"
                                    icon="fa-file-upload"
                                    :disabled="isArchived"
                                    @click="linkStore.toggleModal"
                                >
                                    Upload your first {{ type === 'images' ? 'image' : 'protocol' }}
                                </VaButton>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
                <!-- No Results from Search -->
                <div v-else-if="!linkStore.links.length && linkStore.filter" class="flex lg12 md12 sm12 xs12">
                    <VaCard class="empty-state-card">
                        <VaCardContent>
                            <div class="column align-center text-center">
                                <VaIcon 
                                    name="fa-search"
                                    size="large"
                                    color="neutral"
                                    class="mb-4"
                                />
                                <h3 class="va-h3 mb-2">No results found</h3>
                                <p class="va-text-secondary mb-4">
                                    No {{ type }} match your search "{{ linkStore.filter }}". Try adjusting your search terms.
                                </p>
                                <VaButton
                                    color="textPrimary"
                                    preset="plain"
                                    @click="clearSearch"
                                >
                                    Clear search
                                </VaButton>
                            </div>
                        </VaCardContent>
                    </VaCard>
                </div>
                <!-- Links List -->
                <template v-else>
                    <div v-for="link in linkStore.links" class="flex lg12 md12 sm12 xs12">
                        <LinkDetailsCard @show="handleShow" @delete="triggerDelete" :link="link" :key="link.name"
                            :type="type" />
                    </div>
                    <div v-if="total > linkStore.pagination.limit" class="flex lg12 md12 sm12 xs12 justify-center mt-4">
                        <VaPagination color="textPrimary" v-model="offset" @update:modelValue="handlePagination"
                            :page-size="linkStore.pagination.limit" :total="total" :visible-pages="3"
                            buttons-preset="primary" gapped />
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
                <div class="flex">
                    <VaButton @click="deleteImage" color="danger">
                        Delete
                    </VaButton>
                </div>
            </div>
        </template>
    </VaModal>
    <VaModal hide-default-actions close-button v-model="showImage">
        <div class="layout">
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaImage :fit="'contain'" :src="imageSrc" style="height: 500px;">

                    </VaImage>
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
const imageSrc = ref('')
const protocolToDelete = ref<Record<string, any> | null>(null)


const total = computed(() => linkStore.total)
const isArchived = computed(() => projectStore.isArchived)
const offset = computed({
    get() {
        return linkStore.pagination.offset + 1
    },
    set(v: number) {
        linkStore.pagination.offset = v - 1
    }
})

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

async function handlePagination() {
    await linkStore.fetchProjectModelLinks(props.projectId, props.modelName, props.type)
}

function handleShow(src: string) {
    imageSrc.value = src
    showImage.value = !showImage.value
}
function triggerDelete(protocol: Record<string, any>) {
    protocolToDelete.value = { ...protocol }
    showDeleteConfirmation.value = !showDeleteConfirmation.value
}

async function deleteImage() {
    if (!protocolToDelete.value) return
    await linkStore.deleteLink(props.projectId, props.modelName, protocolToDelete.value.name, props.type)
    showDeleteConfirmation.value = !showDeleteConfirmation.value
    await handleSearch()
    await modelStore.getStats(props.projectId, props.modelName)
}

async function downloadAllFiles() {
    try {
        await linkStore.downloadAllFiles(props.projectId, props.modelName)
    } catch (error) {
        console.error('Error downloading files:', error)
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

.empty-state-card {
    margin: 2rem 0;
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
</style>