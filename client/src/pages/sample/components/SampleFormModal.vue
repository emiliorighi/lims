<template>
    <VaModal hide-default-actions class="modal-crud" :model-value="sampleStore.showForm" @cancel="reset">
        <template #header>
            <h2 class="va-h2">
                {{ sampleStore.update ? `Editing Sample ${sampleStore.sample?.sample_id}` : 'Creating Sample' }}
            </h2>
        </template>
        <!-- 
            id logic -> if not update
                compute ordered id
                check sample exists

            id fields -> if not update
                check required

            required fields
                
            optional fields
        

        -->
        <VaForm v-if="sampleStore.sample" ref="sampleForm">

            <div class="row">
                <VaInput class="flex lg8 md8" readonly label="Unique identifier" v-model="sampleId"
                    placeholder="The unique identifier will be generated here"
                    :rules="[requiredIdRule, !sampleExists || 'Sample Id already exists']">
                </VaInput>
            </div>

            <VaDivider />
            <div style="max-height: 400px;overflow: scroll;">
                <div v-for="field in sampleFields" :key="field.key" class="row">

                    <div v-if="isInputField(field.filter)" class="flex lg6 md6">
                        <VaInput class="mt-4" :disabled="disabledRule(field)" :messages="[field.description]"
                            :label="field.label" v-model="sampleStore.sample.metadata[field.key]"
                            :rules="[requiredFieldRule(field.label, field.required)]" />
                    </div>

                    <div v-else-if="isSelectField(field.filter)" class="flex lg6 md6">
                        <VaSelect class="mt-4" :disabled="disabledRule(field)" :messages="[field.description]"
                            :label="field.label" v-model="sampleStore.sample.metadata[field.key]"
                            :multiple="field.filter.multi" :options="field.filter.choices"
                            :rules="[requiredSelectRule(field.label, field.required)]" />
                    </div>

                    <div v-else-if="isRangeField(field.filter)" class="flex lg8 md8">
                        <VaSlider class="mt-4" :disabled="disabledRule(field)" :label="field.label"
                            :max="field.filter.max" :min="field.filter.min"
                            v-model="sampleStore.sample.metadata[field.key]" track-label-visible>
                            <template #trackLabel="{ value }">
                                <VaChip color="warning" size="small">
                                    {{ value }}
                                </VaChip>
                            </template>
                        </VaSlider>
                        <VaInput class="mt-4" :rules="[requiredNumberFieldRule(field.label, field.required)]" :messages="[field.description]"
                            readonly v-model="sampleStore.sample.metadata[field.key]">
                            <template #appendInner>
                                <span>{{ field.filter.unit }}</span>
                            </template>
                        </VaInput>
                    </div>
                </div>
                <VaDivider />
                <div class="row justify-space-between">
                    <div class="flex">
                        <VaButton icon="save" @click="saveSample">Save</VaButton>
                    </div>
                    <div class="flex">
                        <VaButton color="danger" @click="reset" icon="cancel">Cancel</VaButton>
                    </div>
                </div>
            </div>
        </VaForm>
    </VaModal>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../../stores/schemas-store';
import { useSampleStore } from '../../../stores/sample-store';
import { Filter, Input, Select, Range } from '../../../data/types'
import { computed, onMounted, ref, watch } from 'vue';
import SampleService from '../../../services/clients/SampleService'
import { useGlobalStore } from '../../../stores/global-store';
import { AxiosError } from 'axios';
import { useForm } from 'vuestic-ui/web-components';

const { validate } = useForm('sampleForm')


// Rules for validation
const requiredIdRule = (v: string) => v.length > 0 || 'Fill the required fields to generate the unique identifier'
const requiredFieldRule = (label: string, required = true) => (v: any) => !required || !!v || `${label} is required`;
const requiredSelectRule = (label: string, required = true) => (v: any) => !required || (Array.isArray(v) && v.length > 0) || (!!v) || `${label} is required`;
const requiredNumberFieldRule = (label: string, required = true) => (v: any) => !required || !isNaN(v) || `${label} must be a number`;

const emits = defineEmits(['onSampleEdited'])
const { schema } = useSchemaStore()
const sampleStore = useSampleStore()

const sampleExists = ref(false)
const sampleFields = ref<Filter[]>([...schema.sample.fields])


const disabledRule = (filter: Filter) => sampleStore.update && schema.sample.id_format.includes(filter.key)

const { toast } = useGlobalStore()

const sampleId = computed(() => {
    return Object.entries(sampleStore.sample?.metadata || {})
        .filter(([k, v]) => {
            // Ensure 'v' is a valid value and the key is included in the id_format
            if (schema.sample.id_format.includes(k) && v !== null && v !== undefined && v !== '') {
                // Check if 'v' is a number or a string
                return typeof v === 'string' || typeof v === 'number';
            }
            return false;
        })
        .map(([k, v]) => {
            // Ensure toString() conversion for numbers for joining purposes
            return v.toString();
        })
        .join('_');
});

watch(() => sampleId.value, async () => {

    if (sampleId.value.length < 2 || sampleStore.update) return

    await getSample(sampleId.value)

})

async function saveSample() {
    if (!validate()) {
        toast({
            color: 'danger',
            message: 'Form is not valid',
        });
        return
    }

    if (sampleStore.update) {
        await updateSample()
    } else {
        await createSample()
    }

}

async function updateSample() {
    try {

        if (!sampleStore.sample) return

        const { sample_id, metadata } = sampleStore.sample
        const { data } = await SampleService.updateSample(schema.project_id, sample_id, metadata)
        toast({
            color: 'success',
            message: Array.isArray(data) ? data.join(', ') : 'Sample updated successfully',
        });

        sampleStore.sample = null
        sampleStore.update = false
        sampleStore.showForm = false
        emits('onSampleEdited')


    } catch (error) {
        console.error('Error updating sample:', error);

        let message = 'Impossible to update';
        if (error instanceof AxiosError) {
            message = error.response?.data?.message || message;
        }

        toast({
            color: 'danger',
            message,
        });
    }
}

async function createSample(): Promise<void> {
    try {
        if (!sampleStore.sample) return

        const { metadata } = sampleStore.sample
        const response = await SampleService.createSample(schema.project_id, metadata);
        const { data } = response;

        toast({
            color: 'success',
            message: Array.isArray(data) ? data.join(', ') : 'Sample created successfully',
        });

        sampleStore.sample = null
        sampleStore.update = false
        sampleStore.showForm = false

        emits('onSampleEdited')

        // reset();
        // emits('onSampleEdited');
    } catch (error) {
        console.error('Error creating sample:', error);

        let message = 'Impossible to save';
        if (error instanceof AxiosError) {
            message = error.response?.data?.message || message;
        }

        toast({
            color: 'danger',
            message,
        });
    }
}

async function getSample(id: string): Promise<void> {

    try {
        const response = await SampleService.getSample(schema.project_id, id);
        const { data } = response;
        if (data) sampleExists.value = true
        toast({
            message: `Sample ${id} already exists`,
            color: 'danger',
        });
    } catch (error) {
        if (error instanceof AxiosError) {
            if (error.response?.status !== 404) {
                // Sample is new

                console.error('Error:', error);
                toast({
                    message: error.response?.data?.message,
                    color: 'danger',
                });
            } else {
                sampleExists.value = false
            }
        } else {
            console.error('Unexpected error:', error);
            toast({
                message: 'An unexpected error occurred',
                color: 'danger',
            });
        }
    }
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


function reset() {
    sampleFields.value = []
    sampleStore.sample = null
    sampleFields.value = [...schema.sample.fields]
    sampleStore.update = false
    sampleStore.showForm = false
}
</script>
