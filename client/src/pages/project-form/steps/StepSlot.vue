<template>
    <div class="step-slot">
        <div class="row row-equal">
            <div class="flex lg12 md12 sm12 xs12">
                <IdFieldsCard :model="model" />
            </div>
        </div>
        <div class="row row-equal">
            <div class="flex lg12 md12 sm12 xs12">
                <AttributeCRUDTable :model="model" />
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import IdFieldsCard from '../../../components/cards/IdFieldsCard.vue';
import AttributeCRUDTable from '../../../components/tables/AttributeCRUDTable.vue';

const props = defineProps<{
    model: 'sample' | 'experiment'
}>()

</script>
