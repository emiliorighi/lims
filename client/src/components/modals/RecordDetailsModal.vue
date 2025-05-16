<template>
    <VaModal v-model="recordStore.showRecordDetails" close-button>
        <template #header>
            <h3 class="va-h3">
                Details of Record: {{ recordId }}
            </h3>
        </template>
        <div v-if="recordEntries.length" class="layout va-gutter-5 fluid">
            <div class="row">
                <div v-for="dEntry in defaultEntries" :key="dEntry.label" class="flex lg6 md6 sm12 xs12">
                    <p class="va-text-secondary">
                        <VaIcon size="small" :name="dEntry.icon" /> {{ dEntry.label }}
                    </p>
                    <p>{{ dEntry.value }}</p>
                </div>
            </div>
            <VaDivider>Attributes</VaDivider>
            <div class="row">
                <div v-for="attr in attributes" :key="attr.key" class="flex lg6 md6 sm12 xs12">
                    <p class="va-text-secondary">
                        <VaIcon size="small" :name="attr.icon" />
                        {{ attr.key }}

                        <VaBadge v-if="attr.isIdField" color="warning" text="ID Field">

                        </VaBadge>
                    </p>
                    <p v-if="Array.isArray(attr.value)">{{ attr.value.join(', ') }}</p>
                    <p v-else>{{ attr.value }}</p>
                </div>
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useRecordStore } from '../../stores/record-store';
import { ResearchFilter, ResearchModel } from '../../data/types';
import { formatDate } from '../../composables/formatDate';

const props = defineProps<{
    referenceModel?: ResearchModel | null
    fields: ResearchFilter[]
    idFields: string[]
}>()

const recordStore = useRecordStore()
const recordEntries = computed(() => Object.entries(recordStore.record ?? {}))
const recordId = computed(() => recordStore.record?.item_id)
const iconMap = {
    project_id: 'fa-diagram-project',
    model_name: 'fa-cube',
    created: 'fa-calendar',
    created_by: 'fa-user',
    reference_id: 'fa-up-right-from-square'
}

const defaultEntries = computed(() => recordEntries.value
    .filter(([k, v]) => k in iconMap)
    .map(([k, v]: any) =>
        ({ icon: iconMap[k as keyof typeof iconMap], value: k === 'created' ? formatDate(new Date(v.$date)) : v, label: k === 'reference_id' ? `${props.referenceModel?.name} Id` : k })
    ))

const attributes = computed(() => props.fields
    .filter(({ key }) => recordEntries.value.find(([k, _]) => key === k))
    .map(({ key, type }) => {
        const entry = recordEntries.value.find(([k, _]) => k === key)
        const icon = type === 'select' ? 'fa-tag' : type === 'date' ? 'fa-calendar' : type === 'number' ? 'fa-hashtag' : 'fa-edit'
        return { value: entry?.[1], key, icon, isIdField: props.idFields.includes(key) }
    })
)

</script>
<style scoped>
p {
    padding: 0.5rem;
}
</style>