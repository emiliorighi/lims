<template>
  <VaDateInput clearable :format-date="formatDate" :label="field.key" style="width: 100%;" mode="range"
    v-model="rangeDates" @update:model-value="emitRangeDates" />
</template>

<script setup lang="ts">
import { ref, toRefs, onMounted } from 'vue';

const props = defineProps<{
  field: { key: string };
  value: Record<string, any>;
}>();

const emits = defineEmits<{
  (e: 'update', value: Record<string, any>): void;
}>();

const gteKey = `${props.field.key}__gte`;
const lteKey = `${props.field.key}__lte`;


// Values from parent
const payload = toRefs(props).value;
const rangeDates = ref<{ start: Date | null; end: Date | null }>({ start: null, end: null });

onMounted(() => {
  if (payload.value[gteKey] || payload.value[lteKey]) {
    rangeDates.value = {
      start: parseDate(payload.value[gteKey]),
      end: parseDate(payload.value[lteKey])
    };
  }
});


function emitRangeDates(range: { start: Date | null; end: Date | null } | undefined) {
  emits('update', {
    [gteKey]: range?.start ? formatDate(range.start) : null,
    [lteKey]: range?.end ? formatDate(range.end) : null
  });
}
// --- Helpers
function formatDate(date: Date): string {
  const y = date.getFullYear();
  const m = `${date.getMonth() + 1}`.padStart(2, '0');
  const d = `${date.getDate()}`.padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function parseDate(str: string | undefined): Date | null {
  if (!str) return null;
  const [y, m, d] = str.split('-').map(Number);
  return new Date(y, m - 1, d);
}
</script>