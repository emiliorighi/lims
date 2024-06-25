<template>
    <VaInnerLoading :loading="isLoading">
        <div class="row justify-space-between">
            <div class="flex">
                Create filters or upload them from a TSV file
            </div>
            <div class="flex">
                <div class="row justify-space-between">
                    <div class="flex">
                        <VaFileUpload style="z-index: 0" :color="errorMessage ? 'danger' : 'primary'" v-model="tsv"
                            file-types=".tsv" type="single" undo uploadButtonText="Upload TSV" />
                    </div>
                    <div class="flex">
                        <VaCounter v-model="treshold" :min="0" :max="100" :step="5"
                            messages="Percentage treshold of select field inferring" />

                    </div>
                </div>
            </div>
        </div>
    </VaInnerLoading>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue';
import { useAttributeStore } from '../../../../../stores/attribute-store'
import ProjectService from '../../../../../services/clients/ProjectService'
import { Filter } from '../../../../../data/types';
import { useToast } from 'vuestic-ui/web-components'


const tsv = ref<undefined | File>()
const errorMessage = ref('')
const treshold = ref(25)
const attributeStore = useAttributeStore()
const isLoading = ref(false)
const { init } = useToast()

watch(() => tsv.value, async () => {
    if (tsv.value) inferAttributes(tsv.value)
})

async function inferAttributes(tsv: File) {
    try {
        isLoading.value = !isLoading.value
        const formData = new FormData()
        formData.append('tsv', tsv)
        formData.append('treshold', treshold.value.toString())
        const { data } = await ProjectService.inferAttributesProject(formData)
        attributeStore.attributes = [
            ...attributeStore.attributes,
            ...data
                .filter(
                    (dF: Filter) =>
                        attributeStore.attributes
                            .every(
                                (aF: Filter) => dF.key !== aF.key)
                )
        ]
    } catch (error) {
        console.error(error)
        init({ message: 'Error inferring attributes from tsv', color: 'danger' })
    } finally {
        isLoading.value = !isLoading.value

    }
}


</script>