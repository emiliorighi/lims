<template>
    <VaSelect :label="field.key" multiple @clear="fetchOptions" :loading="isLoading" @open="fetchOptions" clearable
        v-model="modelValue" :options="optionsKeys">
        <template #option="{ option, selectOption }">
            <div :class="['row option align-center justify-space-between', modelValue.includes(option as any) ? 'is-active' : '']"
                @click="selectOption(option)">
                <div class="flex">
                    <p>{{ option }}</p>
                </div>
                <div v-if="options" class="flex">
                    <VaChip size="small">
                        {{ options[option as string] }}
                    </VaChip>
                </div>
            </div>
        </template>
        <template #content="{ value }">
            <VaChip v-for="chip in value.slice(0, 3)" :key="chip" size="small" outline color="textPrimary">
                {{ chip }}
            </VaChip>
        </template>
    </VaSelect>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRecordStore } from '../../stores/record-store';

const recordStore = useRecordStore()

const props = defineProps<{
    label?: string,
    field: { key: string },
    modelName: string,
    projectId: string,
    value: string | null,
}>()

const emits = defineEmits(['valueChange'])


const isLoading = ref(false)

const modelValue = computed({
    get() {
        if (props.value)
            return props.value.split(',')
        return []
    },
    set(values: string[]) {
        emits('valueChange', values.length > 0 ? values.join(',') : null)
    }
})

const options = ref<Record<string, number> | null>(null)

const optionsKeys = computed(() => Object.keys(options.value ?? {}))

async function fetchOptions() {
    isLoading.value = true
    const opts = await recordStore.getFieldFrequencies(props.projectId, props.modelName, props.field)
    options.value = { ...opts }
    isLoading.value = false
}

</script>
<style scoped>
.option {
    cursor: pointer;
    padding: 5px;
}

.option:hover {
    background-color: #dee5f2;
    /* Background color on hover */
}

.is-active {
    background-color: #dee5f2;

}
</style>