<template>
    <VaModal v-model="linkStore.showLinkForm" hideDefaultActions close-button>
        <template #header>
            <h3 class="va-h3 va-text-capitalize">
                Upload {{ type }}
            </h3>
        </template>
        <div class="layout fluid va-gutter-5">
            <VaForm ref="linkForm">
                <div class="row">
                    <div class="flex lg12 md12 sm12 xs12">
                        <p v-if="!files.length" class="va-text-danger">
                            Upload at least one file
                        </p>
                        <VaFileUpload :color="files.length ? 'textPrimary' : 'danger'" dropzone
                            :label="`Upload ${type}`" v-model="files" @update:model-value="handleUpdate" type="gallery">
                        </VaFileUpload>
                    </div>
                </div>
                <div v-for="file, idx in linkStore.files" :key="file.file.name" class="row">
                    <div class="flex lg12 md12 sm12 xs12">
                        <VaCard outlined>
                            <VaCardTitle>
                                <div class="row justify-space-between">
                                    <div class="flex">
                                        {{ file.file.name }}
                                    </div>
                                    <div class="flex">
                                        <VaButton color="danger" size="small" icon="fa-trash" @click="handleDelete(idx)"></VaButton>
                                    </div>
                                </div>

                            </VaCardTitle>
                            <VaImage v-if="type === 'images'" style="height: 200px;" :src="file.preview" />
                            <VaCardContent>
                                <div class="row">
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <VaInput label="Name"
                                            :rules="[(v: string) => !!v || 'Name is Mandatory', (v: string) => names.filter(n => v === n).length <= 1 || `${v} already defined`]"
                                            v-model="file.name" placeholder="Name" />
                                    </div>
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <VaTextarea label="Description" style="width: 100%;" v-model="file.description"
                                            placeholder="Image description" />
                                    </div>
                                </div>
                            </VaCardContent>
                        </VaCard>
                    </div>
                </div>
            </VaForm>
        </div>
        <template #footer>
            <div class="row justify-space-between">
                <div class="flex">
                    <VaButton @click="linkStore.toggleModal" color="textPrimary" preset="primary">Close Form</VaButton>
                </div>
                <div class="flex">
                    <VaButton @click="handleSubmit">Submit</VaButton>
                </div>
            </div>
        </template>
    </VaModal>

</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useForm, useToast } from 'vuestic-ui/web-components';
import { useModelStore } from '../../stores/model-store';
import { useLinkStore } from '../../stores/link-store';
import { LinkType } from '../../data/types';
import { success, catchError } from '../../composables/toastMessages';
import LinkService from '../../services/clients/LinkService';

const props = defineProps<{
    projectId: string
    modelName: string
    type: LinkType
}>()

const { init } = useToast()
const { validate } = useForm('linkForm')
const linkStore = useLinkStore()
const loading = ref(false)
const files = ref<File[]>([])

const names = computed(() => linkStore.files.map(({ name }) => name))
const isImage = computed(() => props.type === 'images')
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
            linkStore.toggleModal()
            await modelStore.getStats(props.projectId, props.modelName)
            linkStore.resetFilters()
            await linkStore.fetchProjectModelLinks(props.projectId, props.modelName, props.type)
        }

    }
}

function handleDelete(idx: number) {
    linkStore.files = [...linkStore.files.slice(0, idx), ...linkStore.files.slice(idx + 1)]
}

function handleUpdate(files: File[]) {
    linkStore.files = [...files.map(file => ({ name: file.name, file, description: '', type: props.type, preview: isImage.value ? URL.createObjectURL(file) : undefined }))]
}
</script>
