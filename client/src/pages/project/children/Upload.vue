<template>
    <VaCard>
        <VaInnerLoading :loading="isLoading">
            <VaCardContent>
                <VaAccordion v-model="accordionState" multiple>
                    <!-- TSV Upload Section -->
                    <VaCollapse icon="upload_file" header="TSV Upload">
                        <ModelSelector :behaviour="behaviour" :model="model" @update:model="(v: ModelType) => model = v"
                            @update:behaviour="(v: string) => behaviour = v" />
                        <TSVUploader :model="model" :tsv="tsv" @update:tsv="(v: any) => tsv = v" />
                    </VaCollapse>

                    <!-- Column Mapping Section -->
                    <VaCollapse :disabled="mappedFields.length === 0" icon="checklist" header="Column Mapping">
                        <ColumnMapping :mapped-fields="mappedFields" :model="model"
                            @update:mapped-fields="updateMappedFields" />

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
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useSchemaStore } from '../../../stores/schemas-store';
import { useToast } from 'vuestic-ui/web-components';
import ProjectService from '../../../services/clients/ProjectService';
import { AxiosError } from 'axios';
import { ModelType } from '../../../data/types'
import ModelSelector from '../../../components/forms/ModelSelector.vue'
import TSVUploader from '../../../components/forms/TSVUploader.vue';
import ColumnMapping from '../../../components/forms/ColumnMapping.vue'
import AuthService from '../../../services/clients/AuthService';

const schemaStore = useSchemaStore();
const isLoading = ref(false);
const tsv = ref();
const behaviour = ref('SKIP');
const model = ref<ModelType>('sample');
const accordionState = ref([true, false]);

const { init, } = useToast();


const mappedFields = ref<{
    tsv_column: string,
    field_key: string | null
}[]>([]);

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


const sampleId = computed(() => {
    const sampleID = mappedFields.value.find(f => f.field_key === 'sample_id')
    if (sampleID) return sampleID.tsv_column
    return undefined
})


// Watchers
watch(() => tsv.value, async () => {
    if (tsv.value) await fetchHeaderMap(schemaStore.schema.project_id);
});

watch(() => model.value, async () => {
    if (tsv.value) await fetchHeaderMap(schemaStore.schema.project_id);
});


function updateMappedFields(payload: { tsvColumn: string, value: string }) {
    const f = mappedFields.value.find(({ tsv_column }) => payload.tsvColumn === tsv_column)
    if (f) {
        f.field_key = payload.value
    }
}
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
        const { data } = await AuthService.uploadTSV(schemaStore.schema.project_id, formData);
        init({ message: data, color: 'success' });
        resetForm();
    } catch (error) {
        console.log(error)
        const axiosError = error as AxiosError;
        const responseData = axiosError.response?.data as { message: string }
        let message
        if (responseData && responseData.message) {
            message = responseData.message
        } else {
            message = `Error importing ${model.value}s`
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