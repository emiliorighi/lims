<template>
    <Header :title="title" />
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaInnerLoading :loading="isLoading">

                    <VaCardContent>

                        <VaAccordion v-model="accordionState" multiple>

                            <!-- TSV Upload Section -->
                            <VaCollapse icon="upload_file" header="TSV Upload">

                                <div class="row">
                                    <VaSelect class="flex lg6 md6 sm12 xs12" :disabled="validModels.length === 1"
                                        v-model="model" :options="validModels" :messages="['The model in use']">
                                        <template #prependInner>
                                            <VaIcon class="mr-1" :color="model === 'sample' ? 'success' : 'primary'"
                                                :name="modelIcon" />
                                        </template>
                                    </VaSelect>

                                    <VaSelect class="flex lg6 md6 sm12 xs12" v-model="behaviour"
                                        :messages="[`SKIP or UPDATE existing ${model}s`]"
                                        :options="['SKIP', 'UPDATE']" />
                                </div>

                                <div class="row mt-4">
                                    <VaFileUpload class="flex lg12 md12 sm12 xs12" v-model="tsv" dropzone
                                        style="z-index: 0" file-types=".tsv" type="single" undo
                                        :uploadButtonText="`Upload ${model}s`" />
                                </div>


                            </VaCollapse>

                            <!-- Column Mapping Section -->
                            <VaCollapse :disabled="mappedFields.length === 0" icon="checklist" header="Column Mapping">


                                <div class="row">
                                    <VaInput clearable class="flex lg4 md6 sm12 xs12" placeholder="Search a column..."
                                        v-model="filter" />
                                    <div v-for="field in fields" :key="field.label" class="flex">
                                        <VaButtonDropdown preset="primary" :color="field.color" :label="field.label">
                                            <ul>
                                                <li class="p-6" v-for="f in field.items" :key="f">{{ f }}</li>
                                            </ul>
                                        </VaButtonDropdown>
                                    </div>
                                    <div v-if="model === 'experiment' && !sampleId" class="flex">
                                        <VaButton preset="primary" color="danger">{{ 'SampleID is Missing' }}
                                        </VaButton>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="flex lg12 md12 sm12 xs12">
                                        <VaDataTable :items="mappedFields" :columns="['tsv_column', 'field_key']"
                                            :filter="filter" :filter-method="customFilteringFn">
                                            <template #cell(tsv_column)="{ value }">
                                                <VaInput :model-value="value" read-only />
                                            </template>
                                            <template #cell(field_key)="{ value, row }">
                                                <VaSelect :class="getFieldClass(value)" clearable searchable
                                                    highlight-matched-text track-by="text" value-by="text"
                                                    text-by="text" :options="fieldOptions" :model-value="value"
                                                    @update:modelValue="(v: string) => row.rowData.field_key = v">
                                                    <template #prepend>
                                                        <VaIcon v-if="isDuplicate(value)" name="warning"
                                                            color="danger" />
                                                        <VaIcon v-else-if="!!value" name="check_circle"
                                                            color="success" />
                                                    </template>
                                                </VaSelect>
                                            </template>
                                        </VaDataTable>
                                    </div>
                                </div>
                            </VaCollapse>
                        </VaAccordion>
                    </VaCardContent>
                    <VaCardActions align="between">
                        <VaButton color="danger" @click="resetMap">Reset</VaButton>
                        <VaButton @click="handleSubmit" :disabled="isSubmitDisabled">
                            Submit
                        </VaButton>
                    </VaCardActions>
                </VaInnerLoading>

            </VaCard>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useSchemaStore } from '../../../stores/schemas-store';
import { useToast } from 'vuestic-ui/web-components';
import ProjectService from '../../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import Header from '../../../components/ui/Header.vue'
import { ModelType } from '../../../data/types'

const props = defineProps<{
    title: string
}>()
const schemaStore = useSchemaStore();
const isLoading = ref(false);
const tsv = ref();
const behaviour = ref('SKIP');
const model = ref<ModelType>('sample');
const filter = ref('');
const accordionState = ref([true, false]);

const { init, } = useToast();

type InferMap = {
    tsv_column: string,
    field_key: string | null
};

const mappedFields = ref<InferMap[]>([]);

const ICONS = {
    ADD: 'add_circle',
    BUILD: 'build_circle',
    ERROR: 'error'
};

// Computed Properties
const validModels = computed(() => {
    if (schemaStore.schema.experiment.id_format.length === 0) return ['sample'];
    return ['sample', 'experiment'];
});

const modelIcon = computed(() => {
    return model.value === 'sample' ? 'fa-vial' : 'fa-dna';
});

const duplicates = computed(() => {
    const fieldKeyCount: Record<string, number> = {};
    mappedFields.value.forEach(({ field_key }) => {
        if (field_key) fieldKeyCount[field_key] = (fieldKeyCount[field_key] || 0) + 1;
    });
    return Object.keys(fieldKeyCount).filter(key => fieldKeyCount[key] > 1);
});

const requiredFields = computed(() => {
    const filledFields = mappedFields.value.map(({ field_key }) => field_key).filter(f => f);
    return schemaStore.schema[model.value].fields.filter(f => f.required && !filledFields.includes(f.key));
});

const optionalFields = computed(() => {
    const filledFields = mappedFields.value.map(({ field_key }) => field_key).filter(f => f);
    return schemaStore.schema[model.value].fields.filter(f => !f.required && !filledFields.includes(f.key));
});

const sampleId = computed(() => {
    const sampleID = mappedFields.value.find(f => f.field_key === 'sample_id')
    if (sampleID) return sampleID.tsv_column
    return undefined
})

const fields = computed(() => {
    const validFields = [];
    if (duplicates.value.length) {
        validFields.push({
            label: 'Duplicated fields',
            color: 'danger',
            items: [...duplicates.value]
        });
    }
    if (requiredFields.value.length) {
        validFields.push({
            label: 'Required fields',
            color: 'danger',
            items: [...requiredFields.value.map(({ key }) => key)]
        });
    }
    if (optionalFields.value.length) {
        validFields.push({
            label: 'Optional fields',
            color: 'secondary',
            items: [...optionalFields.value.map(({ key }) => key)]
        });
    }
    return validFields;
});

const fieldOptions = computed(() => {
    const schemaModel = schemaStore.schema[model.value];
    const filteredF = mappedFields.value.map(({ field_key }) => field_key).filter(f => f);
    const parsedFields = schemaModel.fields.map(f => ({
        text: f.key,
        icon: schemaModel.id_format.includes(f.key) ? ICONS.BUILD : f.required ? ICONS.ERROR : ICONS.ADD,
        disabled: filteredF.includes(f.key)
    }));
    if (model.value === 'experiment') parsedFields.push({
        text: 'sample_id',
        icon: ICONS.ERROR,
        disabled: filteredF.includes('sample_id')
    })
    return parsedFields
});

// Watchers
watch(() => tsv.value, async () => {
    if (tsv.value) await fetchHeaderMap(schemaStore.schema.project_id);
});

watch(() => model.value, async () => {
    if (tsv.value) await fetchHeaderMap(schemaStore.schema.project_id);
});

// Methods
async function fetchHeaderMap(projectId: string) {
    try {
        isLoading.value = true;
        const formData = new FormData();
        formData.append('tsv', tsv.value);
        formData.append('model', model.value);
        const { data } = await ProjectService.inferHeadersFromTSV(projectId, formData);
        mappedFields.value = [...data];
        accordionState.value = [false, true];
    } catch (error) {
        console.error(error);
        init({ message: 'Error mapping project...', color: 'danger', duration: 1500 });
    } finally {
        isLoading.value = false;
    }
}

function isDuplicate(value: string) {
    return duplicates.value.includes(value);
}

function getFieldClass(value: string) {
    return isDuplicate(value) ? 'va-input-wrapper--error' : value ? 'va-input-wrapper--success' : '';
}

function customFilteringFn(source: string) {
    if (!filter.value) return true;
    return new RegExp(filter.value, 'i').test(source);
}

function resetMap() {
    mappedFields.value.forEach(m => (m.field_key = ''));
}

async function handleSubmit() {
    const formData = new FormData();
    formData.append('file', tsv.value);
    formData.append('model', model.value);
    formData.append('behaviour', behaviour.value);
    const stringifiedFields = mappedFields.value
        .filter(f => f.field_key)
        .map(({ tsv_column, field_key }) => `${tsv_column}:${field_key}`)
        .join(',');
    formData.append('map', stringifiedFields);

    try {
        isLoading.value = true;
        const { data } = await ProjectService.uploadTSV(schemaStore.schema.project_id, formData);
        init({ message: data, color: 'success' });
        resetForm();
    } catch (error) {
        const axiosError = error as AxiosError;
        const responseData = axiosError.response?.data as { message: string }
        let message
        if (responseData.message) {
            message = responseData.message
        } else {
            message = 'Error importing samples'
        }
        init({ message, color: 'danger' });
    } finally {
        isLoading.value = false;
    }
}

function resetForm() {
    tsv.value = undefined;
    model.value = 'sample';
    behaviour.value = 'SKIP';
    mappedFields.value = [];
}

const isSubmitDisabled = computed(() => {
    if (model.value === 'experiment') return requiredFields.value.length || duplicates.value.length || !sampleId.value
    return requiredFields.value.length || duplicates.value.length
});

</script>