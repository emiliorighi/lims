<template>
    <!-- <TsvImport/> -->
    <!-- <DragAndDrop/> -->
    <TableFilters :columns="columns" :fields="schemaStore.schema.sample.fields" @on-filter-change="updateSearchForm"
        @on-show-field-change="updateShowFields" />
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <va-card :stripe="Boolean(errorMessage)" stripe-color="danger">
                <va-skeleton v-if="isLoading" height="400px" />
                <va-card-content v-else-if="errorMessage">
                    {{ errorMessage }}
                </va-card-content>
                <va-card-content v-else>
                    <CRUDTable :items="samples" :columns="columns" @edit-clicked="editSample" @new-clicked="newSample"
                        @delete-clicked="deleteSample" />
                    <VaDivider />
                    <Pagination @offset-changed="handlePagination" :limit="sampleStore.pagination.limit"
                        :off-set="sampleStore.pagination.offset" :total="total" />
                </va-card-content>
            </va-card>
        </div>
    </div>
    <ModelForm :schema-model="schemaStore.schema.sample" :valid-id-callback="SampleService.getSample"
        :is-update="sampleStore.isUpdate" :model="sampleStore.sample" v-if="schemaStore.schema.project_id" />
    <SampleForm @on-sample-edited="reset" v-if="schemaStore.schema.project_id" />
</template>

<script setup lang="ts">
import { useSampleStore } from '../../stores/sample-store';
import { useSchemaStore } from '../../stores/schemas-store';
import SampleForm from './SampleForm.vue';
import { computed, onMounted, ref, watchEffect } from 'vue';
import { Filter, Input, SampleModel, Select, Range, ModelSearchForm } from '../../data/types';
import SampleService from '../../services/clients/SampleService';
import { useGlobalStore } from '../../stores/global-store';
import ModelForm from '../../components/modals/ModelForm.vue'
import TableFilters from '../../components/filters/TableFilters.vue'
import CRUDTable from '../../components/data/CRUDTable.vue'
import Pagination from '../../components/filters/Pagination.vue'
import TsvImport from '../../components/forms/TsvImport.vue';
import DragAndDrop from '../../components/forms/DragAndDrop.vue';
const props = defineProps<{
    projectId: string
}>()

const defaultSample: SampleModel = {
    sample_id: '',
    metadata: {}
}
const schemaStore = useSchemaStore()
const sampleStore = useSampleStore()
const { toast } = useGlobalStore()

function newSample() {
    sampleStore.sample = { ...defaultSample }
}
watchEffect(async () => {
    const { filters, ...sortFields } = sampleStore.searchForm
    const validFilters = Object.fromEntries(Object.entries(filters).filter(([k, v]) => v))
    getSamples({ ...validFilters, ...sortFields, ...sampleStore.pagination })
})

const showFields = ref(schemaStore.schema.sample.fields.map((filter: Filter) => {
    return {
        show: filter.required,
        value: filter.key
    }
}))

const columns = computed(() => {
    return ['sample_id', ...showFields.value.filter(f => f.show).map(f => `metadata.${f.value}`), 'actions']
})

function updateSearchForm(payload: ModelSearchForm) {
    sampleStore.searchForm = { ...payload }
}

function updateShowFields(updatedShowFields: { show: boolean, value: string }[]) {
    showFields.value = [...updatedShowFields]
}

const samples = ref<SampleModel[]>([])
const total = ref(0)
const errorMessage = ref('')
const isLoading = ref(false)
const offset = ref(1 + sampleStore.pagination.offset)

onMounted(() => {
    // const { filters, ...sortFields } = sampleStore.searchForm
    // getSamples({ ...filters, ...sortFields, ...sampleStore.pagination })
})


function handleSubmit() {
    sampleStore.resetPagination()
    offset.value = 1
    getSamples({ ...sampleStore.searchForm, ...sampleStore.pagination })
}

function handlePagination(value: number) {
    sampleStore.pagination.offset = value - 1
    getSamples({ ...sampleStore.searchForm, ...sampleStore.pagination })
}

function editSample(index: number) {
    sampleStore.isUpdate = true
    sampleStore.sample = { ...samples.value[index] }
}

async function deleteSample(index: number) {
    try {
        const sampleToDelete = samples.value[index]
        const { data } = await SampleService.deleteSample(props.projectId, sampleToDelete.sample_id)
        toast({ message: data.message, color: 'success', duration: 1500 })
    } catch (error) {
        toast({ message: 'Error', color: 'danger', duration: 1500 })
    } finally {
        reset()
    }
}

// async function submitSample(metadata: Record<string, any>) {
//     const { sample } = sampleStore
//     try {
//         if (sampleStore.isUpdate) {
//             const { data } = await SampleService.updateSample(props.projectId, sample.sample_id, sample.metadata)
//             toast({ color: 'success', message: data.join(', '), duration: 1500 })

//         } else {
//             const { data } = await SampleService.createSample(schema.project_id, sample.metadata)
//             toast({ color: 'success', message: data.join(', '), duration: 1500 })
//         }
//         emits('onSampleEdited')
//     } catch (error) {
//         toast({ color: 'danger', message: 'Impossible to save', duration: 1500 })
//     } finally {
//         resetSample()
//     }
// }

function reset() {
    offset.value = 1
    sampleStore.resetSeachForm()
    sampleStore.resetPagination()
    getSamples({ ...sampleStore.pagination })
}

async function getSamples(query: Record<string, any>) {
    try {
        const { data } = await SampleService.getSamples(schemaStore.schema.project_id, query)
        samples.value = data.data
        total.value = data.total
    } catch (e) {
        errorMessage.value = 'Something happened'
    } finally {
        isLoading.value = false
    }
}
</script>
<style scoped>
.w-200 {
    width: 200px;
}
</style>