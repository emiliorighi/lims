<template>
    <VaButton preset="primary" icon="upload_file" @click="show = !show" color="secondary">Upload TSV</VaButton>
    <VaModal v-model="show" hide-default-actions>
        <template #header>
            <h2 class="va-h2"> TSV Upload</h2>
        </template>
        <VaDivider />
        <VaInnerLoading :loading="isLoading">
            <VaFileUpload dropzone type="single" label="Upload TSV" v-model="tsv" file-types=".tsv">
            </VaFileUpload>
        </VaInnerLoading>
        <template #footer>
            <div class="row justify-end">
                <div class="flex">
                    <VaButton :disabled="tsv === undefined" @click="inferAttributes">Submit</VaButton>
                </div>
            </div>
        </template>
    </VaModal>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useAttributeStore } from './../../stores/attribute-store'
import ProjectService from './../../services/clients/ProjectService'
import { Filter } from './../../data/types';
import { useToast } from 'vuestic-ui/web-components'

const tsv = ref<undefined | File>()
const attributeStore = useAttributeStore()
const { init } = useToast()
const show = ref(false)
const file = ref<File>()
const isLoading = ref(false)

async function inferAttributes() {
    if (!tsv.value) return;

    isLoading.value = true;

    try {
        const olderAttributes = [...attributeStore.attributes];
        attributeStore.attributes = [];

        const formData = new FormData();
        formData.append('tsv', tsv.value);

        const { data } = await ProjectService.inferAttributesProject(formData);

        // Filter out new attributes that don't already exist in olderAttributes
        const newAttributes = data.filter(
            (dF: Filter) => !olderAttributes.some((aF: Filter) => dF.key === aF.key)
        );

        // Update the attribute store with combined attributes
        attributeStore.attributes = [...olderAttributes, ...newAttributes];

    } catch (error) {
        console.error('Error inferring attributes from TSV:', error);
        init({ message: 'Error inferring attributes from TSV', color: 'danger' });
    } finally {
        isLoading.value = false;
        show.value = !show.value
    }
}



</script>
