<template>
    <VaInput :key="selectedField" iconColor="primary" @update:modelValue="updateValue" v-model="filter" clearable
        :placeholder="'Search by ' + selectedField">
        <template #prependInner>
            <VaSwitch style="--va-switch-checker-background-color: #ffffff;" color="primary" off-color="success"
                size="small" v-if="isExperiment" v-model="selectedField" true-value="experiment_id"
                false-value="sample_id">
                <template #innerLabel>
                    <div class="va-text-center">
                        <VaIcon :name="selectedField === 'experiment_id' ? 'fa-dna' : 'fa-vial'" />
                    </div>
                </template>
            </VaSwitch>
        </template>
    </VaInput>
</template>
<script setup lang="ts">
import { computed, ref, watchEffect } from 'vue';
import { debounce } from '../../composables/debounce'
import { ModelType } from '../../data/types';

const props = defineProps<{
    model: ModelType
}>()

const selectedField = ref('')
const filter = ref('')
const isExperiment = computed(() => props.model === 'experiment')

watchEffect(() => {
    if (isExperiment.value) selectedField.value = 'experiment_id'
    else selectedField.value = 'sample_id'
})

const emits = defineEmits(['valueChange'])

// Create a debounced version of the emits function
const debouncedEmit = debounce((field: string, value: string) => {
    emits('valueChange', { field, value });
}, 200);

function updateValue(value: string) {
    debouncedEmit(selectedField.value, value);
}
</script>