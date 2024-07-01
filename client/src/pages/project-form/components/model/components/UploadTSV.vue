<template>
    <VaInnerLoading :loading="isLoading">
        <div class="row">
            <div class="flex lg3 md4">
                <VaFileUpload dropzone style="z-index: 0" :color="errorMessage ? 'danger' : 'primary'" v-model="tsv"
                    file-types=".tsv" type="single" undo uploadButtonText="Upload TSV" />
            </div>
            <div class="flex lg3 md4">
                <VaCounter v-model="treshold" :min="0" :max="100" :step="5"
                    messages="Percentage treshold of select field inferring" />
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
import { useDebouncedRef } from "../../../../../composables/debounce.js";




const tsv = ref<undefined | File>()
const errorMessage = ref('')
const treshold = useDebouncedRef(25)
const attributeStore = useAttributeStore()
const isLoading = ref(false)
const { init } = useToast()

watch(() => tsv.value, async () => {
    if (tsv.value) await inferAttributes()
})

watch(() => treshold.value, async () => {
    if (tsv.value) await inferAttributes()
})


async function inferAttributes() {
    try {
        if (!tsv.value) return
        isLoading.value = !isLoading.value
        const olderAttibutes = [...attributeStore.attributes]
        attributeStore.attributes = []
        const formData = new FormData()
        formData.append('tsv', tsv.value)
        formData.append('treshold', treshold.value.toString())
        const { data } = await ProjectService.inferAttributesProject(formData)
        attributeStore.attributes = [
            ...olderAttibutes,
            ...data
                .filter(
                    (dF: Filter) =>
                        olderAttibutes
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