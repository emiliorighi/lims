<template>
    <h4 class="va-h4">Filters Creation</h4>
    <p class="va-text-secondary">Create filters or upload them, then link them to the target model. Filters can be
        imported by multiple TSVs</p>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <AttributesTable />
        </div>
    </div>
    <AttributeFormModal />
</template>
<script setup lang="ts">
import { computed, watch, onMounted } from 'vue'
import { Filter } from '../../../data/types'
import { useAttributeStore } from '../../../stores/attribute-store'
import { useProjectStore } from '../../../stores/project-store'
import AttributesTable from '../../../components/tables/AttributesTable.vue'
import AttributeFormModal from '../../../components/modals/AttributeFormModal.vue'

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
