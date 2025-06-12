<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <div class="row align-center justify-space-between mb-4">
                <div class="flex">
                    <h3 class="va-h3 va-text-capitalize">
                        Upload {{ type }}
                    </h3>
                </div>
                <div class="flex">
                    <VaButton @click="router.back()" color="textPrimary" preset="primary">Back</VaButton>
                </div>
            </div>
            <div class="layout fluid va-gutter-5">
                <VaForm ref="linkForm">
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <p v-if="!files.length" class="va-text-danger">
                                Upload at least one file
                            </p>
                            <VaFileUpload :color="files.length ? 'textPrimary' : 'danger'" dropzone
                                :label="`Upload ${type}`" v-model="files" @update:model-value="handleUpdate">
                            </VaFileUpload>
                        </div>
                    </div>
                    <div v-for="file, idx in linkStore.files" :key="file.file.name" class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaCard>
                                <VaCardBlock horizontal class="flex-wrap">
                                    <VueFilesPreview :file="file.preview" height="300px" width="300px" />
                                    <div class="flex-auto">
                                        <VaCardContent>
                                            <div class="row justify-space-between align-center">
                                                <div class="flex">
                                                    <VaInput label="Name"
                                                        :rules="[(v: string) => !!v || 'Name is Mandatory', (v: string) => names.filter(n => v === n).length <= 1 || `${v} already defined`]"
                                                        v-model="file.name" placeholder="Name" />
                                                </div>
                                                <div class="flex">
                                                    <VaButton preset="primary" @click="handleDelete(idx)" icon="fa-trash"
                                                        color="danger" />
                                                </div>
                                            </div>
                                        </VaCardContent>
                                        <VaCardContent>
                                            <VaTextarea label="Description" style="width: 100%;"
                                                v-model="file.description" placeholder="File description" />
                                        </VaCardContent>
                                        <VaCardContent>
                                            <div class="row justify-space-between align-center">
                                                <div class="flex">
                                                    <div class="row align-center">
                                                        <div class="flex">
                                                            <VaChip size="small" flat color="textPrimary"
                                                                icon="fa-file">
                                                                {{ file.file.name }}
                                                            </VaChip>
                                                        </div>
                                                        <div class="flex">
                                                            <VaChip size="small" flat color="textPrimary"
                                                                icon="fa-file">
                                                                {{ file.file.name.split('.').pop() }}
                                                            </VaChip>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </VaCardContent>
                                    </div>
                                </VaCardBlock>
                            </VaCard>
                        </div>
                    </div>
                </VaForm>
            </div>
            <div class="row justify-end mt-4">
                <div class="flex">
                    <VaButton @click="handleSubmit" :loading="loading">Submit</VaButton>
                </div>
            </div>
        </div>
    </div>

    <!-- Preview Modal -->
    <VaModal hide-default-actions close-button v-model="showImage" size="large">
        <div class="layout">
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VueFilesPreview :file="imageSrc" />
                </div>
            </div>
        </div>
    </VaModal>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useForm, useToast } from 'vuestic-ui/web-components';
import { useModelStore } from '../stores/model-store';
import { useLinkStore } from '../stores/link-store';
import { LinkType } from '../data/types';
import { success, catchError } from '../composables/toastMessages';
import LinkService from '../services/clients/LinkService';
import { VueFilesPreview } from 'vue-files-preview';
import { useRouter } from 'vue-router';

const router = useRouter()
const { init } = useToast()
const { validate } = useForm('linkForm')
const linkStore = useLinkStore()
const loading = ref(false)
const files = ref<File[]>([])
const showImage = ref(false)
const imageSrc = ref<File | undefined>(undefined)
const names = computed(() => linkStore.files.map(({ name }) => name))

const props = defineProps<{
    projectId: string
    modelName: string
    type: LinkType
}>()

const modelStore = useModelStore()

async function handleSubmit() {
    const entries = linkStore.files.map(({ preview, ...data }) => ({ ...data }))
    const hasEmptyName = entries.some(e => !e.name)
    if (!validate() || !entries.length || hasEmptyName) {
        init({ message: 'All files must have a name', color: 'danger' })
        return
    }

    const payload = new FormData()

    entries.forEach((entry, index) => {
        payload.append('files', entry.file)
        payload.append(`metadata[${index}][name]`, entry.name)
        payload.append(`metadata[${index}][description]`, entry.description)
        payload.append(`metadata[${index}][type]`, props.type)
        payload.append(`metadata[${index}][filename]`, entry.file.name)
    })
    let successfull = false
    try {
        loading.value = true
        const { data } = await LinkService.uploadLinks(props.projectId, props.modelName, payload)
        success('Links correctly created', 1500)
        successfull = true
    } catch (err) {
        successfull = false
        catchError(err)
    }
    finally {
        loading.value = false
        if (successfull) {
            await modelStore.getStats(props.projectId, props.modelName)
            linkStore.resetFilters()
            await linkStore.fetchProjectModelLinks(props.projectId, props.modelName, props.type)
            router.back()
        }
    }
}

function handleDelete(idx: number) {
    linkStore.files = [...linkStore.files.slice(0, idx), ...linkStore.files.slice(idx + 1)]
}

function handleUpdate(files: File[]) {
    linkStore.files = [...files.map(file => ({ name: file.name, file, description: '', type: props.type, preview: file }))]
}

function handlePreview(file: File) {
    imageSrc.value = file
    showImage.value = true
}


</script>

<style scoped>
.mb-4 {
    margin-bottom: 1rem;
}

.mt-4 {
    margin-top: 1rem;
}

.justify-end {
    justify-content: flex-end;
}
</style>