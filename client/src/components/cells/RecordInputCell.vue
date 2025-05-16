<template>
    <component v-if="editMode" :is="resolveComponent(item)" style="width: 100%;"
        :model-value="item.type !== 'select' ? value : Array.isArray(value) ? value : value.split(',')"
        :options="item.choices" :placeholder="item.key" :multiple="item.multi" :rules="getFieldRules(item)"
        :messages="[item.description ?? '']" @update:model-value="(v: any) => debouncedUpdate(item, row, v)">
        <template #appendInner v-if="item.type === 'date'">
            <VaIcon color="secondary" name="fa-calendar" />
        </template>
    </component>
    <span v-else>{{ Array.isArray(row.rowData[item.key]) ? row.rowData[item.key].join(', ') :
        row.rowData[item.key]}}</span>
</template>
<script setup lang="ts">
import { ResearchFilter } from '../../data/types';
import AuthService from '../../services/clients/AuthService';
import { useToast, VaInput, VaSelect } from 'vuestic-ui';
import { AxiosError } from 'axios';
import { debounce } from '../../composables/debounce';

const props = defineProps<{
    projectId: string,
    modelName: string,
    editMode: boolean,
    item: ResearchFilter
    value: any,
    row: any
}>()

const { init } = useToast()

/**
 * Dynamically resolves the component based on the item type.
 */
function resolveComponent(item: any) {
    switch (item.type) {
        case 'select':
            return VaSelect;
        case 'date':
            return VaInput;
        default:
            return VaInput;
    }
}

/**
 * Dynamically generates field validation rules.
 */
function getFieldRules(item: any) {
    const rules = [(v: any) => fieldRule(v, item.required, item.regex)];

    if (item.type === 'date') {
        rules.push((v: string) => isValidDate(v, item.required));
    }
    if (item.type === 'number') {
        rules.push((v: number | null) => {
            if (v === null) return true;
            return !isNaN(Number(v)) || "Value must be a valid number";
        });

        rules.push((v: number) => v === 0 || fieldRule(v, item.required, item.regex));
    }

    return rules;
}


const debouncedUpdate = debounce((item: any, row: any, value: any) => {
    if (row.rowData[item.key] === value) return
    row.rowData[item.key] = value
    updateItem(row.rowData.item_id, { [item.key]: value })
}, 500);


async function updateItem(itemId: string, payload: Record<string, any>) {
    try {
        const { data } = await AuthService.updateRecord(props.projectId, props.modelName, itemId, payload)
        init({ message: 'Record correctly updated', color: 'success' })
    } catch (err) {
        const axiosError = err as AxiosError
        const respData = axiosError.response?.data as { message: string }
        init({ message: respData.message, color: 'danger', duration: 10000 })
    }
}

function fieldRule(v: any, required: boolean, regex?: string) {
    if (required && !v) return 'Field is required'
    if (regex && v && !v.toString().match(regex)) return `${v} does not match ${regex}`
    return true
}

function isValidDate(input: string, required: boolean) {
    if (!required && !input) return true //skip validation if field is empty and optional

    // Strict ISO 8601 date format: YYYY-MM-DD
    const isoRegex = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
    if (!isoRegex.test(input)) return "Date should be of ISO format YYYY-MM-DD";

    // Logical date check
    const date = new Date(input);
    const isValid = !isNaN(date.getTime());

    // Check that it still matches after re-formatting (handles Feb 30, etc.)
    const [year, month, day] = input.split('-');
    const formatted = date.toISOString().substring(0, 10);
    return formatted === `${year}-${month}-${day}` && isValid ? true : "Invalid date";
}

</script>