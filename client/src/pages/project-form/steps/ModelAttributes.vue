<template>
    <div class="row justify-space-between align-end">
        <h2 class="va-h2 flex pt-0">Filters creation</h2>
        <div class="flex">
            <div class="row">
                <div class="flex">
                    <UploadTSV />
                </div>
                <div class="flex">
                    <VaButton color="success" @click="attributeStore.initAttribute" icon="add">
                        Filter
                    </VaButton>
                </div>
            </div>
        </div>
    </div>
    <AttributesTable />
    <AttributeFormModal />
</template>
<script setup lang="ts">
import { computed, watch, onMounted } from 'vue'
import { Filter } from '../../../data/types'
import { useAttributeStore } from '../../../stores/attribute-store'
import { useProjectStore } from '../../../stores/project-store'
import AttributesTable from '../../../components/tables/AttributesTable.vue'
import AttributeFormModal from '../../../components/modals/AttributeFormModal.vue'
import UploadTSV from '../../../components/buttons/UploadTSV.vue'

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
