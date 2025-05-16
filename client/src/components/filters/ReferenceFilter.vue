<template>
    <div style="max-height: 150px; overflow: scroll;">
        <VaInnerLoading :loading="isLoading">
            <VaOptionList v-model="modelValue" :options="optionsKeys" />
        </VaInnerLoading>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRecordStore } from '../../stores/record-store';
import StatsService from '../../services/clients/StatsService';

const recordStore = useRecordStore()

const props = defineProps<{
    modelName: string,
    projectId: string,
    value: string | null,
}>()

const emit = defineEmits(['update:value']);

const isLoading = ref(false)

const modelValue = computed({
    get: () => {
        if (props.value)
            return props.value.split(',')
        return []
    },
    set: (val: string[]) => emit('update:value', val.length > 0 ? val.join(',') : null),
});

const options = ref<Record<string, number> | null>(null)

const optionsKeys = computed(() => Object.keys(options.value ?? {}))

onMounted(async () => await fetchOptions())

async function fetchOptions() {
    try {
        isLoading.value = true
        const { data } = await StatsService.getStats(props.projectId, props.modelName, 'reference_id', {})
        options.value = { ...data }
    } catch (err) {
        recordStore.catchError(err)
    } finally {
        isLoading.value = false

    }
}

</script>