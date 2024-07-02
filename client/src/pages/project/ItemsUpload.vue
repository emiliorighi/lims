<template>
    <div class="row row-equal">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard>
                <VaCardTitle class="va-text-secondary mb-0">
                    TSV Upload
                </VaCardTitle>
                <VaCardContent>
                    <div class="row">
                        <div class="flex lg4 md4 sm12 xs12">
                            <VaSelect class="mb-4" :disabled="validOpts.length === 1" v-model="model"
                                :options="validOpts">
                                <template #prependInner>
                                    <VaIcon style="margin-right: 5px;"
                                        :color="model === 'sample' ? 'success' : 'primary'"
                                        :name="model === 'sample' ? 'fa-vial' : 'fa-dna'" />
                                </template>
                            </VaSelect>
                        </div>
                        <div class="flex lg4 md4 sm12 xs12">
                            <VaSelect :messages="['SKIP or UPDATE existing records']" v-model="behaviour"
                                :options="['SKIP', 'UPDATE']">
                            </VaSelect>
                        </div>
                        <div class="flex lg4 md4 sm12 xs12">
                            <VaFileUpload dropzone class="mb-4" style="z-index: 0" v-model="tsv" file-types=".tsv"
                                type="single" undo :uploadButtonText="`Upload ${model}s`" />
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <div v-if="requiredFields.length" class="row align-center">
                        <div class="flex">
                            <VaIcon name="error" color="warning" /> Required Fields:
                        </div>
                        <div v-for="f in requiredFields" class="flex">
                            <VaChip icon="error" color="warning">
                                {{ f.key
                                }}</VaChip>
                        </div>
                    </div>
                    <div class="row align-center">
                        <div class="flex">
                            <VaIcon name="build_circle" :color="idMapped ? 'success' : 'danger'" />{{ model }} ID:
                        </div>
                        <div class="flex">
                            <VaChip icon="build_circle" :color="idMapped ? 'success' : 'danger'">
                                {{ idMapped ? idMapped :
                                schemaStore.schema[model].id_format.join('_') }}</VaChip>
                        </div>
                    </div>
                    <div v-if="duplicates.length" class="row align-center">
                        <div class="flex">
                            <VaIcon name="difference" color="danger" /> Duplicated Fields:
                        </div>
                        <div v-for="d in duplicates" class="flex">
                            <VaChip icon="difference" color="danger">{{ d }}
                            </VaChip>
                        </div>
                    </div>


                </VaCardContent>
                <VaCardContent>
                    <VaInput clearable class="mb-4" placeholder="Search a column.." v-model="filter" />
                    <VaInnerLoading :loading="isLoading">
                        <VaForm ref="itemsUpload">
                            <VaDataTable striped class="table-inline" :items="mappedFields"
                                :columns="['tsv_column', 'field_key']" :filter="filter"
                                :filter-method="customFilteringFn">
                                <template #cell(tsv_column)="{ value, row }">
                                    <VaInput :model-value="value" read-only />
                                </template>
                                <template #cell(field_key)="{ value, row }">
                                    <VaSelect
                                        :class="duplicates.includes(value) ? 'va-input-wrapper--error' : value ? 'va-input-wrapper--success' : ''"
                                        clearable searchable highlight-matched-text track-by="text" value-by="text"
                                        text-by="text" :options="fieldOptions" :model-value="value"
                                        @update:modelValue="(v: string) => row.rowData.field_key = v">
                                        <template #prepend>
                                            <VaIcon v-if="duplicates.includes(value)" name="warning" color="danger" />
                                            <VaIcon v-else-if="!!value" name="check_circle" color="success" />
                                        </template>
                                    </VaSelect>
                                </template>
                            </VaDataTable>
                        </VaForm>
                    </VaInnerLoading>
                </VaCardContent>
                <VaCardActions align="between">
                    <VaButton color="danger" @click="resetMap">Reset</VaButton>
                    <VaButton @click="handleSubmit()" :disabled="requiredFields.length || duplicates.length">
                        Submit
                    </VaButton>
                </VaCardActions>
            </VaCard>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useForm, useToast } from 'vuestic-ui/web-components';
import { computed, ref, watch } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import { VaSelect } from 'vuestic-ui/web-components';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';

const { init } = useToast()
const schemaStore = useSchemaStore()
const isLoading = ref(false)
const tsv = ref()
const header = ref(0)
const behaviour = ref('SKIP')
const { validate } = useForm('itemsUpload')
const model = ref<'sample' | 'experiment'>('sample')
const router = useRouter()
const filter = ref('')

type InferMap = {
    tsv_column: string,
    field_key: string | null
}


const validOpts = computed(() => {
    if (schemaStore.schema.experiment.id_format.length === 0) return ['sample']
    return ['sample', 'experiment']
})

const mappedFields = ref<InferMap[]>([])

const duplicates = computed(() => {
    const fieldKeyCount: Record<string, number> = {};

    for (const inferMap of mappedFields.value) {
        if (inferMap.field_key) {
            fieldKeyCount[inferMap.field_key] = (fieldKeyCount[inferMap.field_key] || 0) + 1;
        }
    }

    // Identify duplicates
    const duplicates: string[] = [];
    for (const [key, count] of Object.entries(fieldKeyCount)) {
        if (count > 1) {
            duplicates.push(key);
        }
    }

    return duplicates;
})

const requiredFields = computed(() => {
    const filledFields = mappedFields.value.map(({ field_key }) => field_key).filter(f => f)
    return schemaStore.schema[model.value].fields.filter(f => f.required && !filledFields.includes(f.key))
})

const idMapped = computed(() => {

    const { id_format } = schemaStore.schema[model.value];

    // Create a mapping from field_key to tsv_column
    const fieldMap = Object.fromEntries(mappedFields.value.map(({ tsv_column, field_key }) => [field_key, tsv_column]));

    // Generate the mapped IDs array by matching field_keys from id_format
    const mappedIds = id_format.map(f => fieldMap[f]).filter(Boolean);

    // If all keys in id_format have corresponding values, join them into a string
    if (mappedIds.length === id_format.length) {
        return mappedIds.join('_');
    }

    return '';
});


watch(() => tsv.value, async () => {
    if (tsv.value) {
        await fetchHeaderMap(schemaStore.schema.project_id)
    }
})

watch(() => model.value, async () => {
    mappedFields.value = []
    if (tsv.value) {
        await fetchHeaderMap(schemaStore.schema.project_id)
    }
})

const ICONS = {
    ADD: 'add_circle',
    BUILD: 'build_circle',
    ERROR: 'error'
};

const fieldOptions = computed(() => {
    const currentModel = model.value
    const schemaModel = schemaStore.schema[currentModel]; // Ensure to type your schema
    const mappedF = mappedFields.value.map(({ field_key }) => field_key).filter(f => f)
    const fields = schemaModel.fields.map(f => {
        const text = f.key;
        let icon = ICONS.ADD;
        let disabled = mappedF.includes(text)
        if (schemaModel.id_format.includes(f.key)) {
            icon = ICONS.BUILD;
        } else if (f.required) {
            icon = ICONS.ERROR;
        }

        return { text, icon, disabled };
    });
    if (model.value === 'experiment') fields.push({
        text: 'sample_id',
        disabled: mappedF.includes('sample_id'),
        icon: ICONS.ERROR
    })
    return fields
});


const customFilteringFn = (source: string, cellData: any) => {

    if (!filter.value) {
        return true;
    }

    const filterRegex = new RegExp(filter.value, "i");

    return filterRegex.test(source);
};



async function fetchHeaderMap(projectId: string) {
    try {
        isLoading.value = true
        const formData = new FormData()
        formData.append('tsv', tsv.value)
        formData.append('model', model.value)
        formData.append('header_row', header.value.toString())
        const { data } = await ProjectService.inferHeadersFromTSV(projectId, formData)
        mappedFields.value = [...data]
        validate()

    } catch (error) {
        console.error(error)
        init({ message: 'Error fetching project..', color: 'danger', duration: 1500 })
    } finally {
        isLoading.value = false
    }

}


function resetMap() {
    mappedFields.value.forEach(m => {
        m.field_key = ''
    })
}

async function handleSubmit() {
    if (!validate()) return

    if (!tsv.value) return


    const formData = new FormData()
    formData.append('file', tsv.value)
    formData.append('model', model.value)
    formData.append('behaviour', behaviour.value)

    //stringify mapped fields tsv_column:id_field 
    const stringifiedFields = mappedFields.value.filter(f => f.field_key).map(({ tsv_column, field_key }) => `${tsv_column}:${field_key}`).join(',')
    formData.append('map', stringifiedFields)


    try {
        isLoading.value = true
        const { data } = await ProjectService.uploadTSV(schemaStore.schema.project_id, formData)
        init({ message: data, color: 'success' })
        reset()
    } catch (error) {
        const axiosError = error as AxiosError
        if (axiosError.response?.data) {
            const message = (axiosError.response.data as { message: string }).message
            init({ message: message, color: 'danger' })
        } else {
            init({ message: 'Error importing samples', color: 'danger' })
        }
    } finally {
        isLoading.value = false
    }
}

function reset() {
    tsv.value = undefined
    model.value = 'sample'
    behaviour.value = 'SKIP'
    mappedFields.value = []
}
</script>
