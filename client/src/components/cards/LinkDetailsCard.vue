<template>
    <VaCard>
        <VaCardBlock horizontal class="flex-wrap">
            <!-- <VaImage class="flex-grow-0 flex-shrink-0 basis-52" src="https://picsum.photos/200" /> -->
            <VaImage class="flex-grow-0 flex-shrink-0 basis-52" v-if="type === 'images'" @click="emits('show', src)"
                lazy fit="cover" style="height: 12rem;" :src="src" />
            <div class="flex-auto">
                <VaCardContent>
                    <div class="row justify-space-between align-center">
                        <div class="flex">
                            <h3 style="word-break: break-all;" class="va-h6">
                                {{ link.name }}
                            </h3>
                            <VaChip v-if="link.extension" size="small" color="backgroundElement">{{ link.extension }}
                            </VaChip>
                        </div>
                        <div class="flex">
                            <VaButton preset="primary" :disabled="isArchived" @click="emits('delete', link)"
                                icon="fa-trash" color="danger" />
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <p class="va-text-secondary">
                        {{ link.description ? link.description : 'No description available' }}
                    </p>
                </VaCardContent>
                <VaCardContent>
                    <div class="row justify-space-between align-center">
                        <div class="flex">
                            <div class="row align-center">
                                <div class="flex">
                                    <VaChip size="small" flat color="textPrimary" icon="fa-user"> {{ link.created_by }}
                                    </VaChip>
                                </div>
                                <div class="flex">
                                    <VaChip size="small" flat color="textPrimary" icon="fa-calendar"> {{ formattedDate
                                        }}
                                    </VaChip>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <div class="row">
                                <div class="flex">
                                    <VaButton v-if="type === 'images'" icon="fa-eye" color="textPrimary"
                                        preset="primary" @click="emits('show', src)">
                                        Preview
                                    </VaButton>
                                </div>
                                <div class="flex">
                                    <VaButton color="textPrimary" preset="primary" block icon="fa-download"
                                        @click="linkStore.downloadFile(link.hash, fileName)">
                                        Download
                                    </VaButton>
                                </div>
                            </div>
                        </div>
                    </div>
                </VaCardContent>
            </div>
        </VaCardBlock>
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


const formattedDate = computed(() => props.link.created ? new Date(props.link.created.$date).toLocaleDateString("en-US") : null)

</script>