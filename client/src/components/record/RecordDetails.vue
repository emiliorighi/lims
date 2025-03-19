<template>
    <VaCard color="backgroundElement">
        <VaCardContent>
            <p> <strong>record id</strong></p>
            <p class="va-text-secondary">{{
                record.item_id }}</p>
        </VaCardContent>
        <VaCardContent v-if="record.reference_id">
            <p> <strong>reference record</strong></p>
            <p class="va-text-secondary">{{
                record.reference_id }}</p>
        </VaCardContent>
        <VaCardContent>
            <p> <strong>project id</strong></p>
            <p>
                {{ record.project_id }}
            </p>
        </VaCardContent>
        <VaCardContent>
            <p> <strong>model name</strong></p>
            <p>
                {{ record.model_name }}
            </p>
        </VaCardContent>
        <VaCardContent>
            <p> <strong>created</strong></p>
            <p>
                {{ formattedDate }}
            </p>
        </VaCardContent>
        <VaCardContent v-for="[k, v] in entries" :key="k">
            <p><strong>{{ k }}</strong></p>
            <p>
                {{ v }}
            </p>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { ResearchRecord } from '../../data/types';

const props = defineProps<{
    record: ResearchRecord
}>()


const staticFields = ['item_id', 'reference_id', 'project_id', 'model_name', 'created', '_id']
const entries = computed(() => Object.entries(props.record).filter(([k, v]) => !staticFields.includes(k)))

const formattedDate = computed(() => new Date(props.record.created.$date).toLocaleDateString("en-US"))

</script>