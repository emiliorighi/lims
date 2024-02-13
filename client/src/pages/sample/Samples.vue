<template>
    <!-- 
        create sample action
        statistics
        filter form
        CRUD table

     -->
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <va-card :stripe="Boolean(errorMessage)" stripe-color="danger">
                <va-card-content>
                    <div class="row justify-space-between align-center">
                        <div class="flex lg4 md4 sm12 xs12">
                            <div class="row">
                                <div class="flex">
                                    <VaButtonDropdown :closeOnContentClick="false" icon="hide_source" round preset="primary"
                                        label="Fields" class="mr-2 mb-2">
                                        <div class="w-200 row justify-center">
                                            <div class="flex" v-for="(field, index) in showFields">
                                                <VaSwitch :key="index" v-model="showFields[index].show" :label="field.value"
                                                    size="small" />
                                            </div>
                                        </div>
                                    </VaButtonDropdown>
                                </div>
                                <div class="flex">
                                    <VaButtonDropdown :closeOnContentClick="false" icon="filter_list" label="Filters" round
                                        preset="primary" class="mr-2 mb-2">
                                        <div class="w-200">
                                            <div v-for="(field, index) in schemaStore.schema.sample.fields" :key="index">
                                                <VaInput :label="field.label" v-if="isInputField(field.filter)"
                                                    v-model="sampleStore.searchForm.filters[field.key]"></VaInput>
                                                <VaSelect :label="field.label" v-else-if="isSelectField(field.filter)"
                                                    v-model="sampleStore.searchForm.filters[field.key]"
                                                    :multiple="field.filter.multi" :options="field.filter.choices">
                                                </VaSelect>
                                                <VaSlider :label="field.label" v-else-if="isRangeField(field.filter)"
                                                    v-model="sampleStore.searchForm.filters[field.key]"
                                                    :min="field.filter.min" :max="field.filter.max" />
                                            </div>
                                        </div>
                                    </VaButtonDropdown>
                                </div>
                                <div class="flex">
                                    <VaButtonDropdown preset="primary" round :closeOnContentClick="false" label="Sort"
                                        icon="sort" class="mr-2 mb-2">
                                        <div class="w-200">
                                            <VaSelect label="Sort Field" v-model="sampleStore.searchForm.sort_column"
                                                :options="columns" />
                                            <VaSelect label="Sort Order" v-model="sampleStore.searchForm.sort_order"
                                                :options="['asc', 'desc']" />
                                        </div>
                                    </VaButtonDropdown>
                                </div>
                            </div>
                        </div>

                        <div class="flex">
                            <VaButton :round="false" @click="newSample()">New Sample</VaButton>
                        </div>
                    </div>
                </va-card-content>
                <!-- <FilterForm :search-form="biosampleStore.searchForm" :filters="filters" @on-submit="handleSubmit" @on-reset="reset" /> -->
                <va-card-content>
                    <div class="row align-center justify-space-between">
                        <div class="flex">
                            <div class="row justify-center">
                                <div v-for="(key, index) in Object.keys(sampleStore.searchForm.filters)" class="flex"
                                    :index="index">
                                    <VaChip @click="delete sampleStore.searchForm.filters[key]"> {{ key }}: {{
                                        sampleStore.searchForm.filters[key] }}
                                    </VaChip>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            Total: {{ total }}
                        </div>
                    </div>
                </va-card-content>
                <va-skeleton v-if="isLoading" height="400px" />
                <va-card-content v-else-if="errorMessage">
                    {{ errorMessage }}
                </va-card-content>
                <va-card-content v-else>
                    <va-data-table :items="samples" :columns="columns">
                        <template #cell(actions)="{ rowIndex }">
                            <VaButton preset="plain" icon="edit" @click="editSample(rowIndex)" />
                            <VaButton preset="plain" icon="delete" color="danger" class="ml-3" @click="deleteSample(rowIndex)" />
                        </template>
                    </va-data-table>
                    <div class="row align-center justify-center">
                        <div class="flex">
                            <va-pagination v-model="offset" :page-size="sampleStore.pagination.limit" :total="total"
                                :visible-pages="3" buttons-preset="secondary" rounded gapped border-color="primary"
                                @update:model-value="handlePagination" />
                        </div>
                    </div>
                </va-card-content>
            </va-card>
        </div>
    </div>
    <SampleForm @on-sample-edited="reset" v-if="schemaStore.schema.project_id" />
</template>

<script setup lang="ts">
import { useSampleStore } from '../../stores/sample-store';
import { useSchemaStore } from '../../stores/schemas-store';
import SampleForm from './SampleForm.vue';
import { computed, onMounted, ref, watchEffect } from 'vue';
import { Filter, Input, SampleModel, Select, Range } from '../../data/types';
import SampleService from '../../services/clients/SampleService';
import { useGlobalStore } from '../../stores/global-store';
import { Axios, AxiosError } from 'axios';

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
    getSamples({ ...filters, ...sortFields, ...sampleStore.pagination })
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
        const { data } = await SampleService.deleteSample(schemaStore.schema.project_id, sampleToDelete.sample_id)
        toast({message: data.message, color: 'success', duration: 1500})
    } catch (error) {
        toast({message:'Error', color: 'danger', duration: 1500})
    } finally {
        reset()
    }
}

function reset() {
    offset.value = 1
    sampleStore.resetSeachForm()
    sampleStore.resetPagination()
    getSamples({ ...sampleStore.pagination })
}
const isInputField = (filter: Filter['filter']): filter is Input => {
    return (filter as Input).input_type !== undefined;
};

const isSelectField = (filter: Filter['filter']): filter is Select => {
    return (filter as Select).choices !== undefined;
};

const isRangeField = (filter: Filter['filter']): filter is Range => {
    return (filter as Range).min !== undefined;
};
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