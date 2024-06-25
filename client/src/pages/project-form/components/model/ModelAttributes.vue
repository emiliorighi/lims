<template>
    <VaCard>
        <VaCardContent class="va-h4">
            Model filters
        </VaCardContent>
        <VaCardContent class="va-text-secondary">
            Create a list of filters that will be used to define samples and experiments. Optionally, upload a tsv
            file to generate the list of attributes
        </VaCardContent>
        <VaDivider />
        <VaCardContent class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <VaSplit class="split-demo">
                    <template #start>
                        <div class="row">
                            <div class="flex lg12 md12 sm12 xs12">
                                <VaCard square outlined>
                                    <VaCardTitle>Attributes list</VaCardTitle>
                                    <VaCardContent>
                                        <UploadTSV />
                                    </VaCardContent>
                                    <VaCardContent>
                                        <AttributeList />
                                    </VaCardContent>
                                </VaCard>
                            </div>
                        </div>
                    </template>
                    <template #end>
                        <VaSplit class="split-demo">
                            <template #start>
                                <div class="row">
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <ModelAttributeList :columns="modelColumns" :items="sampleAttributes"
                                            title="sample filters" />
                                    </div>
                                </div>
                            </template>
                            <template #end>
                                <div class="row">
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <ModelAttributeList :columns="modelColumns" :items="experimentAttributes"
                                            title="experiment filters" />
                                    </div>
                                </div>
                            </template>
                        </VaSplit>
                    </template>
                </VaSplit>
            </div>
        </VaCardContent>
    </VaCard>
    <AttributeFormModal />
</template>
<script setup lang="ts">
import { computed, watch, onMounted } from 'vue'
import { Filter } from '../../../../data/types'
import AttributeFormModal from './components/AttributeFormModal.vue'
import { useAttributeStore } from '../../../../stores/attribute-store'
import { useProjectStore } from '../../../../stores/project-store'
import UploadTSV from './components/UploadTSV.vue'
import AttributeList from './components/AttributeList.vue'
import ModelAttributeList from './components/ModelAttributeList.vue'

const modelColumns = [
    'key', 'required', 'type'
]
const attributeStore = useAttributeStore()
const projectStore = useProjectStore()


onMounted(() => {
    const sampleAttrs = projectStore.currentProject.sample.fields.map((f) => { return { model: 'sample', ...f } }) as Filter[]
    const expAttrs = projectStore.currentProject.experiment.fields.map((f) => { return { model: 'experiment', ...f } }) as Filter[]
    attributeStore.attributes = [...sampleAttrs, ...expAttrs]

})


const sampleAttributes = computed(() => {
    return attributeStore.attributes.filter(a => a.model && a.model === 'sample').map(({ model, ...fields }) => fields)
})
const experimentAttributes = computed(() => {
    return attributeStore.attributes.filter(a => a.model && a.model === 'experiment').map(({ model, ...fields }) => fields)
})

watch(() => [sampleAttributes.value, experimentAttributes.value], () => {
    projectStore.currentProject.sample.fields = sampleAttributes.value
    projectStore.currentProject.experiment.fields = experimentAttributes.value
})

</script>
