<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <div class="row align-center justify-space-between">
                <div class="flex lg4 md6">
                    <VaInput v-model="linkStore.filter" @update:model-value="debouncedSearch"
                        :placeholder="`Search ${type}...`" clearable>
                    </VaInput>
                </div>
                <div class="flex">
                    <VaButton icon="fa-file-upload" :disabled="isArchived" @click="linkStore.toggleModal">
                        Upload {{ type }}</VaButton>
                </div>
            </div>
            <div class="row row-equal">
                <div v-for="link in linkStore.links" class="flex lg4 md4 sm12 xs12">
                    <LinkDetailsCard @show="handleShow" @delete="triggerDelete" :link="link" :key="link.name"
                        :type="type" />
                </div>
            </div>
            <div class="row justify-center">
                <div class="flex">
                    <VaPagination v-model="offset" @update:modelValue="handlePagination"
                        :page-size="linkStore.pagination.limit" :total="total" :visible-pages="3"
                        buttons-preset="primary" gapped />
                </div>
            </div>
            <!-- <VaCard>
                <VaCardContent>
                    <div class="row align-center justify-space-between">
                        <div class="flex">
                            <VaInput v-model="linkStore.filter" @update:model-value="debouncedSearch"
                                placeholder="Search" clearable>
                            </VaInput>
                        </div>
                        <div class="flex va-text-capitalize">
                            <VaButton :disabled="isArchived" @click="linkStore.toggleModal">
                                Upload {{ type }}</VaButton>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <div class="row row-equal">
                        <div v-for="link in linkStore.links" class="flex lg4 md4 sm12 xs12">
                            <LinkDetailsCard @show="handleShow" @delete="triggerDelete" :link="link" :key="link.name"
                                :type="type" />
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <div class="row justify-center">
                        <div class="flex">
                            <VaPagination v-model="offset" @update:modelValue="handlePagination"
                                :page-size="linkStore.pagination.limit" :total="total" :visible-pages="3"
                                buttons-preset="primary" gapped />
                        </div>
                    </div>
                </VaCardContent>
            </VaCard> -->
        </div>
    </div>
    <VaModal v-model="showDeleteConfirmation" hide-default-actions>
        <template #header>
            <div class="row align-center justify-space-between">
                <div class="flex">
                    <h3 class="va-h3">
                        Deleteting {{ protocolToDelete?.name }}
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
            <VaButton @click="deleteImage" color="danger">
                Confirm </VaButton>
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
</script>