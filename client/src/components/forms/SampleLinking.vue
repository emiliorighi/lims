<template>
    <h6 class="va-h6">Sample Linking</h6>
    <p class="va-text-secondary mb-2">Link this experiment to a sample </p>
    <div class="row">
        <VaSelect class="flex lg6 md6 sm12 xs12 mb-2" :rules="sampleRules" @update:search="handleSearch"
            @update:modelValue="(v: string) => emit('update:value', v)" v-model="metadata.sample_id" :options="samples"
            label="Sample" :loading="selectLoading" dropdownIcon="search" searchable highlight-matched-text
            searchPlaceholderText="Type to search" noOptionsText="No sample found">
        </VaSelect>
    </div>
</template>

<script setup lang="ts">

const props = defineProps<{
    metadata: { sample_id: string }
    samples: string[]
    selectLoading: boolean
}>()

const emit = defineEmits(['update:search', 'update:value'])

const sampleRules = [(v: string) => !!v || 'Sample is mandatory']

function handleSearch(query: string) {
    emit('update:search', query)
}
</script>