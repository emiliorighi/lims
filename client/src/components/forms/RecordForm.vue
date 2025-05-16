<template>
    <VaForm ref="recordForm" tag="tr">
        <td class="layout va-gutter-3" v-if="refModel" colspan="1">
            <ReferenceSelect :model-name="modelName" :project-id="projectId" />
        </td>
        <td v-for="field in fields" :key="field.key" class="layout va-gutter-3" colspan="1">
            <component :is="resolveComponent(field)" v-model="recordStore.recordForm[field.key]"
                :options="field.choices" :placeholder="field.key" :multiple="field.multi" :rules="getFieldRules(field)"
                :messages="[field.description ?? '']">
                <template #appendInner v-if="field.type === 'date'">
                    <VaIcon color="secondary" name="fa-calendar" />
                </template>
            </component>
        </td>
        <td class="layout va-gutter-3" colspan="1">
            <VaButtonGroup>
                <VaButton :loading="isLoading" preset="secondary" @click="handleSubmit" color="success" icon="fa-save">
                </VaButton>
                <VaButton preset="secondary" @click="handleFormReset" style="margin-left: 5px;" color="textPrimary"
                    icon="fa-close">
                </VaButton>
            </VaButtonGroup>
        </td>
    </VaForm>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useModelStore } from '../../stores/model-store';
import { useRecordStore } from '../../stores/record-store';
import AuthService from '../../services/clients/AuthService';
import { useToast, VaInput, VaSelect, useForm } from 'vuestic-ui';
import { AxiosError } from 'axios';
import ReferenceSelect from '../inputs/ReferenceSelect.vue';

const props = defineProps<{
    projectId: string,
    modelName: string,
}>()

const { validate } = useForm('recordForm')
const { init } = useToast()

const recordStore = useRecordStore()
const modelStore = useModelStore()
const fields = computed(() => modelStore.filters)
const refModel = computed(() => modelStore.refModel)
const isLoading = ref(false)
const emit = defineEmits(['submit:success']);

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

function handleFormReset() {
    recordStore.toggleRecordForm()
    recordStore.resetForm()
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

async function handleSubmit() {
    if (!validate()) {
        init({ message: 'Fill the required fields', color: 'danger' })
        return
    }
    const filteredEntries = Object.entries(recordStore.recordForm).filter(
        ([, v]) => v === 0 || (v && !(Array.isArray(v) && v.length === 0))
    );
    let success = false
    try {
        const { data } = await AuthService.createRecord(props.projectId, props.modelName, Object.fromEntries(filteredEntries))
        init({ message: 'Record correctly created', color: 'success' })

        success = true
    } catch (err) {
        success = false
        const axiosError = err as AxiosError
        const respData = axiosError.response?.data as { message: string }
        init({ message: respData.message, color: 'danger', duration: 10000 })
    }
    finally {

        if (!success) return
        emit('submit:success')
    }
}

</script>