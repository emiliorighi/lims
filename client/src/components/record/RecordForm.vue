<template>
    <div v-for="{ title, description, fields } in form" :key="title" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard square outlined>
                <VaCardContent>
                    <div class="row">
                        <div class="flex">
                            <h3 class="va-h5">
                                {{ title }}
                            </h3>
                            <p class="va-text-secondary">
                                {{ description }}
                            </p>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <div class="row">
                        <div v-for="field in fields" :key="field.key" class="flex lg12 md12 sm12 xs12">
                            <VaInput clearable :label="field.key" v-if="field.type === 'text'"
                                v-model="recordStore.recordForm[field.key]"
                                :rules="[(v: string) => fieldRule(v, field.required, field.regex)]"
                                :messages="[field.description ?? '']" :placeholder="field.key" />
                            <VaInput clearable style="width: 100%;" :label="field.key" v-else-if="field.type === 'date'"
                                v-model="recordStore.recordForm[field.key]" :rules="[
                                    (v: any) => fieldRule(v, field.required, field.regex),
                                    (v: string) => isValidDate(v)
                                ]" :messages="[field.description ?? '']" :placeholder="field.key">
                                <template #appendInner>
                                    <VaIcon color="secondary" name="fa-calendar" />
                                </template>
                            </VaInput>
                            <VaSelect clearable :label="field.key" v-else-if="field.type === 'select'"
                                v-model="recordStore.recordForm[field.key]"
                                :rules="[(v: any) => fieldRule(v, field.required)]"
                                :messages="[field.description ?? '']" :placeholder="field.key" :options="field.choices"
                                :multiple="field.multi" />
                            <VaCounter clearable style="width: 100%;" :label="field.key" manual-input buttons
                                v-else-if="field.type === 'number'" v-model="recordStore.recordForm[field.key]" :rules="[(v: number) => v === 0 || fieldRule(v, field.required, field.regex)
                                ]" :messages="[field.description ?? '']" :placeholder="field.key">
                                <template #decreaseAction>
                                    <VaButton icon="fa-minus" color="textPrimary" preset="primary"
                                        @click="recordStore.recordForm[field.key] -= 1">
                                    </VaButton>
                                </template>
                                <template #increaseAction>
                                    <VaButton icon="fa-plus" color="textPrimary" preset="primary"
                                        @click="recordStore.recordForm[field.key] += 1">
                                    </VaButton>
                                    <VaButton @click="recordStore.recordForm[field.key] = null" color="textPrimary"
                                        preset="secondary" icon="fa-close"></VaButton>
                                </template>
                            </VaCounter>
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
    <div v-if="referenceModel" class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaCard square outlined>
                <VaCardContent>
                    <div class="row">
                        <div class="flex">
                            <h3 class="va-h5">
                                Reference Record
                            </h3>
                            <p class="va-text-secondary">
                                Search and select the reference record
                            </p>
                        </div>
                    </div>
                </VaCardContent>
                <VaCardContent>
                    <p v-if="noRefenceItems" class="va-text-danger">
                        You need to first create the reference item <VaChip
                            :to="{ name: 'projectModel', params: { projectId, modelName: referenceModel } }"
                            style="margin-left:3px;">here</VaChip>
                    </p>
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaSelect :disabled="noRefenceItems" @update:search="getRecords" searchable
                                searchPlaceholderText="Type to search"
                                noOptionsText="No records found, refine your search criteria"
                                v-model="recordStore.recordForm.reference_id" :options="referenceRecords" clearable
                                :rules="[(v: any) => !!v || 'Field is mandatory']" :loading="searchLoading"
                                textBy="item_id" trackBy="item_id" valueBy="item_id" />
                        </div>
                    </div>
                </VaCardContent>
            </VaCard>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRecordStore } from '../../stores/record-store';
import { ReseachModel, ResearchFilter } from '../../data/types';
import RecordService from '../../services/clients/RecordService';
import { useToast } from 'vuestic-ui/web-components';

const props = defineProps<{
    projectId: string
    model: ReseachModel
    referenceModel?: string
}>()

const { init } = useToast()
const searchLoading = ref(false)
const recordStore = useRecordStore()
const referenceRecords = ref<Record<string, any>[]>([])
const referenceTotal = ref(0)
const noRefenceItems = ref(false)
const modelfields = computed(() => props.model.id_format)
const idToUpdate = computed(() => recordStore.idToUpdate)
const fields = computed(() => props.model.fields)
//
const requiredFields = computed(() => fields.value.filter(f => !modelfields.value.includes(f.key) && f.required))

const optionalFields = computed(() => fields.value.filter(f => !modelfields.value.includes(f.key) && !f.required))

const idFields = computed(() => props.model.fields.filter(f => modelfields.value.includes(f.key)))

const form = computed(() => {
    const f: { title: string, description: string, fields: ResearchFilter[] }[] = []
    if (!idToUpdate.value) f.push(
        {
            title: 'Id Fields',
            description: 'Fields used to generate the unique identifier of the record',
            fields: [...idFields.value]
        }
    )
    if (requiredFields.value.length) f.push(
        {
            title: 'Required Fields',
            description: 'Fields that cannot be left empty',
            fields: [...requiredFields.value]
        }
    )
    if (optionalFields.value.length) f.push(
        {
            title: 'Optional Fields',
            description: 'Fields that can be optionally filled',
            fields: [...optionalFields.value]
        }
    )
    return f
})

function fieldRule(v: any, required: boolean, regex?: string) {
    if (required && !v) return 'Field is required'
    if (regex && v && !v.toString().match(regex)) return `${v} does not match ${regex}`
    return true
}

function isValidDate(date: string): string | boolean {
    // Regular expression for basic MM/DD/YYYY format with valid month and day ranges
    const dateRegex = /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/(19|20)\d{2}$/;

    console.log(date)
    // Check if the format matches
    if (!dateRegex.test(date)) {
        return "Date should be of format MM/DD/YYYY and the year should be between 1900 and 2099";
    }

    // Extract values
    const [month, day, year] = date.split('/').map(Number);

    // Define the number of days in each month (default for non-leap years)
    const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    // Check for leap year adjustment in February
    const isLeapYear = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    if (isLeapYear) {
        daysInMonth[1] = 29; // February gets 29 days in a leap year
    }
    if (day <= daysInMonth[month - 1]) { return true }

    // Validate the day against the correct max days for the month
    return `${day} is not in ${month}`
}

watch(() => fields.value, () => {
    if (!idToUpdate.value) {
        recordStore.initForm(fields.value)
    }
}, { immediate: true })

onMounted(async () => {
    if (props.referenceModel) await getRecords("")
    if (referenceTotal.value === 0) noRefenceItems.value = true
})


async function getRecords(filter: string) {
    if (!props.referenceModel) return
    try {
        searchLoading.value = true
        const { data } = await RecordService.getItems(props.projectId, props.referenceModel, { filter })
        referenceRecords.value = [...data.data]
        referenceTotal.value = data.total
    } catch (err) {
        console.error(err)
        init({ message: 'Error fetching records, check the logs', color: 'danger' })
    } finally {
        searchLoading.value = false
    }
}

</script>
<style>
.va-date-input__dropdown-content {
    z-index: 1000 !important;
}
</style>