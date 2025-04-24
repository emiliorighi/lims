<template>
    <VaDropdown :close-on-content-click="false" stick-to-edges>
        <template #anchor>
            <VaInput :label="field.key" readonly :model-value="displayValue">
                <template #appendInner>
                    <VaIcon v-if="displayValue" name="highlight_off" color="secondary" @click="clear" />
                </template>
            </VaInput>
        </template>
        <VaDropdownContent>
            <div class="layout va-gutter-3 fluid">
                <div class="row justify-end">
                    <div class="flex lg6 md6 sm12 xs12">
                        <VaInput v-model="rangeStart" clearable type="number" inner-label :label="`from ${field.key}`"
                            @update:model-value="emitRange" />
                    </div>
                    <div class="flex lg6 md6 sm12 xs12">
                        <VaInput v-model="rangeEnd" clearable type="number" inner-label :label="`to ${field.key}`"
                            @update:model-value="emitRange" />
                    </div>
                </div>
            </div>
        </VaDropdownContent>
    </VaDropdown>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, toRefs } from 'vue';

const props = defineProps<{
    field: { key: string };
    value: Record<string, any>;
}>();

const emits = defineEmits<{
    (e: 'update', value: Record<string, any>): void;
}>();

const { field, value } = toRefs(props);
const gteKey = `${field.value.key}__gte`;
const lteKey = `${field.value.key}__lte`;
const rangeStart = ref<number | null>(null);
const rangeEnd = ref<number | null>(null);

// Initialize
onMounted(() => {
    if (value.value[gteKey] || value.value[lteKey]) {
        rangeStart.value = parseNumber(value.value[gteKey]);
        rangeEnd.value = parseNumber(value.value[lteKey]);
    }
});

const displayValue = computed(() => {

    const start = rangeStart.value != null ? rangeStart.value : '';
    const end = rangeEnd.value != null ? rangeEnd.value : '';
    return start !== '' || end !== '' ? `${start} - ${end}` : '';

});


function emitRange() {
    emits('update', {
        ...(rangeStart.value != null && { [gteKey]: rangeStart.value }),
        ...(rangeEnd.value != null && { [lteKey]: rangeEnd.value })
    });
}

function clear() {
    rangeStart.value = null;
    rangeEnd.value = null;
    emits('update', {});
}

function parseNumber(val: any): number | null {
    const n = Number(val);
    return isNaN(n) ? null : n;
}
</script>