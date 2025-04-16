<template>
    <VaCard>
        <VaCardContent>
            <div class="row justify-space-between align-center">
                <div class="flex">
                    <h3 class="va-h6">
                        {{ link.name }}
                    </h3>
                    <VaChip v-if="link.extension" size="small" outline color="textPrimary">{{ link.extension }}</VaChip>
                </div>
                <div class="flex">
                    <VaButton size="small" preset="primary" :disabled="isArchived" @click="emits('delete', link)"
                        icon="fa-trash" color="danger" />
                </div>
            </div>
        </VaCardContent>
        <VaImage v-if="type === 'images'" @click="emits('show', src)" lazy fit="cover" style="height: 200px;"
            :src="src" />
        <VaCardContent>
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <p class="va-text-secondary">
                        {{ link.description ? link.description : 'No description available' }}
                    </p>
                </div>
            </div>
        </VaCardContent>
        <VaCardActions align="stretch" vertical>
            <VaButton v-if="type === 'images'" icon="fa-eye" color="textPrimary" preset="primary" block
                @click="emits('show', src)">
                Preview
            </VaButton>
            <VaButton preset="primary" block icon="fa-download" @click="linkStore.downloadFile(link.hash, fileName)">
                Download
            </VaButton>
        </VaCardActions>
        <!-- <div class="row justify-end">
            <div v-if="type === 'images'" class="flex lg6 md6 sm12 xs12">
                <VaButton icon="fa-eye" color="textPrimary" preset="primary" block @click="emits('show', src)">
                    Preview
                </VaButton>
            </div>
            <div v-if="fileName" class="flex lg6 md6 sm12 xs12">
                <VaButton preset="primary" block icon="fa-download"
                    @click="linkStore.downloadFile(link.hash, fileName)">
                    Download
                </VaButton>
            </div>
        </div> -->
    </VaCard>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { FileModelLink, LinkType } from '../../data/types';
import { useProjectStore } from '../../stores/project-store';
import { useLinkStore } from '../../stores/link-store';

const props = defineProps<{
    link: FileModelLink,
    type: LinkType,
    color?: string
}>()

const linkStore = useLinkStore()
const projectStore = useProjectStore()
const emits = defineEmits(['delete', 'show'])

const baseURL = import.meta.env.VITE_API_PATH ?
    import.meta.env.VITE_API_PATH : import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL + 'api' : import.meta.env.BASE_URL + '/api'


const src = computed(() => `${baseURL}/files/${props.link.hash}/download`)
//get extension from path
const fileName = computed(() => props.link.extension ? `${props.link.name}.${props.link.extension}` : props.link.name)
const isArchived = computed(() => projectStore.isArchived)


</script>