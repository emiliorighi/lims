<template>
    <div class="row">
        <VaInput clearable class="flex lg4 md6 sm12 xs12" placeholder="Search a column..." v-model="filter" />
        <div v-for="field in fields" :key="field.label" class="flex">
            <VaButtonDropdown preset="primary" :color="field.color" :label="field.label">
                <ul>
                    <li class="p-6" v-for="f in field.items" :key="f">{{ f }}</li>
                </ul>
            </VaButtonDropdown>
        </div>
        <div v-if="model === 'experiment' && !sampleId" class="flex">
            <VaButton preset="primary" color="danger">{{ 'SampleID is Missing' }}</VaButton>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaDataTable :items="mappedFields" :columns="['tsv_column', 'field_key']" :filter="filter"
                :filter-method="customFilteringFn">
                <template #cell(tsv_column)="{ value }">
                    <VaInput :model-value="value" read-only />
                </template>
                <template #cell(field_key)="{ value, row }">
                    <!-- <VaSelect :class="getFieldClass(value)" clearable searchable highlight-matched-text track-by="text"
                        value-by="text" text-by="text" :options="fieldOptions" :model-value="value"
                        @update:modelValue="(v: string) => row.rowData.field_key = v">
                        <template #prepend>
                            <VaIcon v-if="isDuplicate(value)" name="warning" color="danger" />
                            <VaIcon v-else-if="!!value" name="check_circle" color="success" />
                        </template>
</VaSelect> -->
                    <VaSelect :class="getFieldClass(value)" clearable searchable highlight-matched-text track-by="text"
                        value-by="text" text-by="text" :options="fieldOptions" :model-value="value"
                        @update:modelValue="(v: string) => $emit('update:mappedFields', { tsvColumn: row.rowData.tsv_column, value: v })">
                        <template #prepend>
                            <VaIcon v-if="isDuplicate(value)" name="warning" color="danger" />
                            <VaIcon v-else-if="!!value" name="check_circle" color="success" />
                        </template>
                    </VaSelect>
                </template>
            </VaDataTable>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useSchemaStore } from '../../stores/schema-store';
import { ModelType } from '../../data/types'

const props = defineProps<{
    model: ModelType,
    mappedFields: { tsv_column: string, field_key: string | null }[],
}>();

const emit = defineEmits(['update:mappedFields']);

const schemaStore = useSchemaStore();

const filter = ref('');

const sampleId = computed(() => {
    const sampleID = props.mappedFields.find(f => f.field_key === 'sample_id')
    if (sampleID) return sampleID.tsv_column
    return undefined
})

const duplicates = computed(() => {
    const fieldKeyCount: Record<string, number> = {};
    props.mappedFields.forEach(({ field_key }) => {
        if (field_key) fieldKeyCount[field_key] = (fieldKeyCount[field_key] || 0) + 1;
    });
    return Object.keys(fieldKeyCount).filter(key => fieldKeyCount[key] > 1);
});

const requiredFields = computed(() => {
    const filledFields = props.mappedFields.map(({ field_key }) => field_key).filter(f => f);
    return schemaStore.schema[props.model].fields.filter(f => f.required && !filledFields.includes(f.key));
});

const optionalFields = computed(() => {
    const filledFields = props.mappedFields.map(({ field_key }) => field_key).filter(f => f);
    return schemaStore.schema[props.model].fields.filter(f => !f.required && !filledFields.includes(f.key));
});

const fields = computed(() => {
    const dups = duplicates.value
    const reqs = requiredFields.value.map(({ key }) => key)
    const opts = optionalFields.value.map(({ key }) => key)
    const validFields = [
        {
            label: 'Duplicated fields',
            color: 'danger',
            items: [...dups]
        },
        {
            label: 'Required fields',
            color: 'danger',
            items: [...reqs]
        },
        {
            label: 'Optional fields',
            color: 'secondary',
            items: [...opts]
        }
    ]
    return validFields.filter(f => f.items.length);
});


const fieldOptions = computed(() => {
    const schemaModel = schemaStore.schema[props.model];
    const filteredF = props.mappedFields.map(({ field_key }) => field_key).filter(f => f);
    const parsedFields = schemaModel.fields.map(f => ({
        text: f.key,
        icon: schemaModel.id_format.includes(f.key) ? 'build_circle' : f.required ? 'error' : 'add_circle',
        disabled: filteredF.includes(f.key)
    }));
    if (props.model === 'experiment') parsedFields.push({
        text: 'sample_id',
        icon: 'error',
        disabled: filteredF.includes('sample_id')
    });
    return parsedFields;
});

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


</script>