<template>
    <div>
        <Header :title="title" :description="description"></Header>
        <VaDivider />
        <VaInnerLoading :loading="isLoading">
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard>
                        <VaCardContent>
                            <h4 class="va-h4">Upload TSV</h4>
                            <p class="va-text-secondary">Upload a TSV file containing sample metadata</p>
                            <VaFileUpload dropzone dropzone-text="Upload a TSV here" style="z-index: 0" v-model="tsv"
                                icon="upload" file-types=".tsv" type="single" undo uploadButtonText="Upload TSV" />
                        </VaCardContent>
                        <VaCardContent>
                            <h4 class="va-h4">Edit the cell values</h4>
                            <p class="va-text-secondary">Map the TSV column to the corresponding field</p>
                            <div class="row align-center justify">
                                <div v-if="requiredFields.length" class="flex">
                                    <VaChip icon="error" color="warning">
                                        Missing
                                        Fields: {{
            requiredFields.length }}
                                    </VaChip>
                                </div>
                                <div class="flex">
                                    <VaChip icon="build_circle" :color="idMapped ? 'success' : 'danger'">
                                        {{ idMapped ? idMapped :
            'MappedID' }}</VaChip>
                                </div>
                                <div v-if="duplicates.length" class="flex">
                                    <VaChip icon="difference" color="danger">
                                        Duplicated fields: {{ duplicates.length }}</VaChip>
                                </div>
                            </div>
                            <div class="row">
                                <div class="flex lg12 md12 sm12 xs12">
                                    <div class="row">
                                        <VaInput clearable class="flex lg4 md6 sm12 xs12"
                                            placeholder="Search a column.." v-model="filter" />
                                    </div>
                                    <VaForm ref="samplesUpload">
                                        <VaDataTable striped class="table-inline" :items="mappedFields"
                                            :columns="['tsv_column', 'field_key']" :filter="filter"
                                            :filter-method="customFilteringFn">
                                            <template #cell(tsv_column)="{ value, row }">
                                                <VaInput :model-value="value" read-only />
                                            </template>
                                            <template #cell(field_key)="{ value, row }">
                                                <VaSelect
                                                    :class="duplicates.includes(value) ? 'va-input-wrapper--error' : value ? 'va-input-wrapper--success' : ''"
                                                    clearable searchable highlight-matched-text track-by="text"
                                                    value-by="text" text-by="text" :options="fieldOptions"
                                                    :model-value="value"
                                                    @update:modelValue="(v: string) => row.rowData.field_key = v">
                                                    <template #prepend>
                                                        <VaIcon v-if="duplicates.includes(value)" name="warning"
                                                            color="danger" />
                                                        <VaIcon v-else-if="!!value" name="check_circle"
                                                            color="success" />
                                                    </template>
                                                </VaSelect>
                                            </template>
                                        </VaDataTable>
                                    </VaForm>
                                </div>
                            </div>
                        </VaCardContent>
                        <VaCardActions align="between">
                            <VaButton color="danger" @click="resetMap">Reset</VaButton>
                            <VaButton @click="handleSubmit" :disabled="requiredFields.length || duplicates.length">
                                Submit
                            </VaButton>
                        </VaCardActions>
                    </VaCard>
                </div>
            </div>
        </VaInnerLoading>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useForm, useToast } from 'vuestic-ui/web-components';
import { computed, onMounted, ref, watch } from 'vue';
import ProjectService from '../../services/clients/ProjectService';
import Header from '../../components/ui/Header.vue';
import { VaSelect } from 'vuestic-ui/web-components';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';

const { init } = useToast()
const schemaStore = useSchemaStore()
const isLoading = ref(false)
const tsv = ref()
const header = ref(0)
const behaviour = ref('SKIP')
const { validate } = useForm('samplesUpload')

const router = useRouter()
const filter = ref('')

type InferMap = {
    tsv_column: string,
    field_key: string | null
}
const props = defineProps<{
    projectId: string
}>()

const title = 'Samples Upload'
const description = 'Upload Samples from a TSV for ' + props.projectId

const mappedFields = ref<InferMap[]>([])


onMounted(async () => {
    if (!schemaStore.schema.project_id) {
        await fetchSchema(props.projectId)
    }
})


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
    return schemaStore.schema.sample.fields.filter(f => f.required && !filledFields.includes(f.key))
})

const idMapped = computed(() => {

    const { id_format } = schemaStore.schema.sample;

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

const ICONS = {
    ADD: 'add_circle',
    BUILD: 'build_circle',
    ERROR: 'error'
};

const fieldOptions = computed(() => {
    const schema = schemaStore.schema; // Ensure to type your schema
    const mappedF = mappedFields.value.map(({ field_key }) => field_key).filter(f => f)
    console.log(mappedF)
    return schema.sample.fields.map(f => {
        const text = f.key;
        let icon = ICONS.ADD;
        let disabled = mappedF.includes(text)
        console.log(disabled)
        if (schema.sample.id_format.includes(f.key)) {
            icon = ICONS.BUILD;
        } else if (f.required) {
            icon = ICONS.ERROR;
        }

        return { text, icon, disabled };
    });
});


const customFilteringFn = (source: string, cellData: any) => {

    if (!filter.value) {
        return true;
    }

    const filterRegex = new RegExp(filter.value, "i");

    return filterRegex.test(source);
};

async function fetchSchema(projectId: string) {
    try {
        isLoading.value = true
        const { data } = await ProjectService.getProject(projectId)
        schemaStore.schema = {
            ...data
        }
    } catch (error) {
        console.error(error)
        init({ message: 'Error fetching project..', color: 'danger', duration: 1500 })
    } finally {
        isLoading.value = false
    }
}

async function fetchHeaderMap(projectId: string) {
    try {
        isLoading.value = true
        const formData = new FormData()
        formData.append('tsv', tsv.value)
        formData.append('model', 'sample')
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
    formData.append('model', 'sample')
    formData.append('behaviour', behaviour.value)

    //stringify mapped fields tsv_column:id_field 
    const stringifiedFields = mappedFields.value.filter(f => f.field_key).map(({ tsv_column, field_key }) => `${tsv_column}:${field_key}`).join(',')
    formData.append('map', stringifiedFields)


    try {
        isLoading.value = true
        const { data } = await ProjectService.uploadTSV(schemaStore.schema.project_id, formData)
        init({ message: data, color: 'success' })
        router.push({ name: 'samples', params: { projectId: props.projectId } })

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
</script>
