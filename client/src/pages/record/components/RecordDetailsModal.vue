<template>
    <VaModal v-model="recordStore.showRecordDetails" noDismiss hideDefaultActions close-button>
        <template #header>
            <h3 v-if="record" class="va-h3">
                {{ record.record_id }}
            </h3>
        </template>
        <div v-if="record" class="layout va-gutter-5 fluid">
            <div class="row">
                <div class="flex lg6 md6 sm12 xs12">
                    <p> <strong>project id</strong></p>
                    <p>
                        {{ record.project_id }}
                    </p>
                </div>
                <div class="flex lg6 md6 sm12 xs12">
                    <p> <strong>model name</strong></p>
                    <p>
                        {{ record.model_name }}
                    </p>
                </div>
                <div v-if="record.reference_id" class="flex lg6 md6 sm12 xs12">
                    <p> <strong>{{ referenceModel }}</strong></p>
                    <p> {{ record.reference_id }}
                    </p>
                </div>
                <div class="flex lg6 md6 sm12 xs12">
                    <p> <strong>created</strong></p>
                    <p>
                        {{ formattedDate }}
                    </p>
                </div>
                <div v-for="[k, v] in entries" :key="k" class="flex lg6 md6 sm12 xs12">
                    <p><strong>{{ k }}</strong></p>
                    <p>
                        {{ v }}
                    </p>
                </div>
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useRecordStore } from '../../../stores/record-store';

const props = defineProps<{
    referenceModel?: string
}>()
const recordStore = useRecordStore()
const record = computed(() => recordStore.record)
const staticFields = ['item_id', 'reference_id', 'project_id', 'model_name', 'created', '_id']
const entries = computed(() => Object.entries(record.value ?? {}).filter(([k, v]) => !staticFields.includes(k)))

const formattedDate = computed(() => record.value ? new Date(record.value.created.$date).toLocaleDateString("en-US") : null)

</script>