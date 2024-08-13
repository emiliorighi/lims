<template>
    <VaButton preset="primary" icon="upload_file" @click="show = !show" color="secondary">Upload File</VaButton>
    <VaModal v-model="show" hide-default-actions>
        <template #header>
            <h2 class="va-h2"> Project upload</h2>
        </template>
        <VaDivider />
        <Transition>
            <div v-if="projectIsValid">
                <b>{{ parsedProject?.project_id }}</b>
                <p class="va-text-secondary">Review the project then click confirm to use it or cancel to
                    cancel the
                    action</p>
                <VaDivider />
                <ProjectOverviewCard v-if="parsedProject" :metadata="parsedProject" />
            </div>
            <div v-else>
                <VaInnerLoading :loading="isLoading">
                    <VaFileUpload dropzone type="single" label="Upload Yaml" v-model="file"
                        file-types=".yaml,.yml,.json">
                    </VaFileUpload>
                    <div v-if="errors.length">
                        <b>Error</b>
                        <p v-for="error, index in errors" :key="index">
                            {{ error }}
                        </p>
                    </div>
                </VaInnerLoading>
            </div>
        </Transition>
        <template #footer>
            <div v-if="projectIsValid" class="row justify-space-between">
                <div class="flex">
                    <VaButton icon="check_circle" color="warning" @click="uploadProject">Confirm
                    </VaButton>
                </div>
                <div class="flex">
                    <VaButton icon="cancel" color="secondary" @click="reset">Cancel
                    </VaButton>
                </div>
            </div>
            <div v-else class="row justify-end">
                <div class="flex">
                    <VaButton :disabled="!file" color="warning" @click="submitFile">Submit</VaButton>
                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { SchemaForm } from './../../data/types'
import * as YAML from 'yaml';
import { useGlobalStore } from './../../stores/global-store';
import ProjectOverviewCard from './../../components/project/ProjectOverviewCard.vue';
import ProjectService from './../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import { useProjectStore } from './../../stores/project-store';

const { toast } = useGlobalStore()
const projectStore = useProjectStore()
const show = ref(false)
const file = ref<File>()
const errors = ref<Record<string, any>[]>([])
const isLoading = ref(false)
const parsedProject = ref<SchemaForm>()
const projectIsValid = ref(false)

async function submitFile() {
    if (!file.value) return
    errors.value = []
    try {
        isLoading.value = true
        const text = await file.value.text()
        const { data } = await ProjectService.validateYAMLProject(text)
        if (data) {
            readFile(file.value)
            projectIsValid.value = !projectIsValid.value
        }
    } catch (e) {
        console.log(e)
        const axiosError = e as AxiosError
        if (axiosError.response?.data) {
            errors.value = [...axiosError.response?.data as Record<string, any>[]]
        } else {
            toast({ message: `Error: ${e}`, color: 'danger' })
        }
    } finally {
        isLoading.value = false
    }
}


function uploadProject() {
    if (parsedProject.value) {
        projectStore.incomingProject = { ...parsedProject.value }
        projectStore.confirmOverwrite = !projectStore.confirmOverwrite
        show.value = !show.value
    }
}

function reset() {
    projectIsValid.value = false
    errors.value = []
}

function readFile(fileObj: File) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const yamlContent = e.target?.result
        parsedProject.value = YAML.parse(yamlContent as string) as SchemaForm
    };
    reader.readAsText(fileObj)
}
</script>