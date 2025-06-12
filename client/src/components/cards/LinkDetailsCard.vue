<template>
    <VaCard>
        <VaCardContent>
            <div class="row flex-nowrap">
                <div class="flex">
                    <div class="basis-48 file-placeholder cursor-pointer content-center flex flex-col justify-space-between relative"
                        @click="emits('show', src, link.extension)">
                        <div class="flex-1 flex-d  justify-center w-full">
                            <VaButton size="small" color="textPrimary" preset="secondary" flat icon="fa-eye">
                            </VaButton>
                        </div>
                        <div class="placeholder-footer w-full flex justify-between items-center px-2 py-1">
                            <span class="ext-label">{{ link.extension?.toUpperCase() || '' }}</span>
                        </div>
                    </div>
                </div>
                <div class="flex flex-1">
                    <div class="row flex-nowrap">
                        <div class="flex">
                            <p class="font-semibold word-wrap-anywhere">{{ link.name }}</p>
                            <p class="va-text-secondary font-size-8 mt-1">{{ link.description ?
                                link.description : 'No description available' }}</p>
                        </div>
                        <div class="flex">
                            <VaButton v-if="role === 'admin' || role === 'project_manager' || role === 'data_manager'" size="small" color="danger" preset="primary" icon="fa-trash"
                                @click="emits('delete', link)" />
                        </div>
                    </div>
                    <VaSpacer />
                    <div class="row align-center justify-space-between">
                        <div class="flex" style="padding:.5rem">
                            <div class="row">
                                <div class="flex" style="padding:.5rem">
                                    <VaChip size="small" flat color="secondary" icon="fa-user">{{ link.created_by }}
                                    </VaChip>

                                </div>
                                <div class="flex" style="padding:.5rem">
                                    <VaChip size="small" flat color="secondary" icon="fa-calendar">{{
                                        formattedDate }}
                                    </VaChip>
                                </div>
                            </div>
                        </div>
                        <div class="flex" style="padding:.5rem">
                            <VaButton size="small" color="textPrimary" preset="primary"
                                @click="linkStore.downloadFile(link.hash, fileName)" flat>Download</VaButton>
                        </div>
                    </div>
                </div>
            </div>
        </VaCardContent>
    </VaCard>

</template>
<script setup lang="ts">
import { computed } from 'vue';
import { FileModelLink, LinkType } from '../../data/types';
import { useProjectStore } from '../../stores/project-store';
import { useLinkStore } from '../../stores/link-store';
import { useGlobalStore } from '../../stores/global-store';

const gStore = useGlobalStore()
const role = computed(() => gStore.user.role)

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

const formattedDate = computed(() => props.link.created ? new Date(props.link.created.$date).toLocaleDateString("en-US") : null)

function formatSize(size: number) {
    if (size < 1024) return size + ' B'
    if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
    return (size / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>

<style scoped>
.basis-48 {
    width: 6.5rem;
    min-width: 6.5rem;
    height: 6.5rem;
    min-height: 6.5rem;
    padding: 0.5rem;
}

.items-center {
    align-items: center;
}

.justify-center {
    justify-content: center;
}

.content-center {
    align-content: center;
}

.flex-d {
    display: flex;
}

.flex-row {
    flex-direction: row;
    display: flex;
}

.flex-nowrap {
    flex-wrap: nowrap;
}

.flex-grow-0 {
    flex-grow: 0;
}

.flex-shrink-0 {
    flex-shrink: 0;
}

.cursor-pointer {
    cursor: pointer;
}

.mt-1 {
    margin-top: 0.25rem;
}

.font-size-8 {
    font-size: 0.8rem;
}

.transition-transform {
    transition: transform 0.2s ease-in-out;
}

.transition-opacity {
    transition: opacity 0.2s ease-in-out;
}

.hover\:scale-105:hover {
    transform: scale(1.05);
}

.hover\:opacity-80:hover {
    opacity: 0.8;
}

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.font-semibold {
    font-weight: 600;
}

.truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.gap-1 {
    gap: 0.25rem;
}

.gap-2 {
    gap: 0.5rem;
}

.gap-4 {
    gap: 1rem;
}

.p-3 {
    padding: 0.75rem;
}

.mb-1 {
    margin-bottom: 0.25rem;
}

.mt-2 {
    margin-top: 0.5rem;
}

.ml-2 {
    margin-left: 0.5rem;
}

.file-placeholder {
    background: linear-gradient(135deg, #e0e3ea 0%, #f5f6fa 100%);
    border-radius: 0.5rem;
    box-shadow: 0 0 0 0 transparent;
    transition: box-shadow 0.2s, border 0.2s;
    border: 1.5px solid transparent;
    position: relative;
}

.file-placeholder:hover {
    box-shadow: 0 2px 8px 0 #b3b8c5;
    border: 1.5px solid #1976d2;
}

.placeholder-footer {
    background: rgba(255, 255, 255, 0.85);
    border-bottom-left-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
    color: #555;
    position: absolute;
    left: 0;
    bottom: 0;
    height: 1.5rem;
}

.ext-label {
    color: #1976d2;
    font-weight: 600;
}

.size-label {
    color: #888;
}

.word-wrap-anywhere {
    word-wrap: anywhere;
}
</style>