<template>
    <VaCard stripe stripe-color="danger">
        <VaCardContent>
            <div class="row align-center">
                <div class="flex">
                    <VaIcon name="fa-exclamation-triangle" color="danger" />
                </div>
                <div class="flex">
                    <h2 class="va-h6">
                        Warning: You are in override mode. Changes made in this mode can potentially break
                        {{
                            totalRecords }} existing record{{ totalRecords !== 1 ? 's' : '' }}{{
                            dependencies.length
                                ? ` and ${dependencies.length} dependent model${dependencies.length !== 1 ? 's' :
                                    ''}` :
                                '' }}.
                    </h2>
                </div>
            </div>
            <div v-if="dependencies.length" class="row mt-2">
                <div class="flex">
                    <p class="va-text-secondary mb-2">
                        Dependent models and their referencing records:
                    </p>
                </div>
                <div v-for="dep in dependencies" :key="dep.key" class="flex lg12 md12 sm12 xs12">
                    <RecordsDeleteCard :columns="dep.columns" :count="dep.value" :model-name="dep.key"
                        :project-id="props.projectId || ''" />
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>

<script setup lang="ts">
import { ResearchModel } from '../../data/types';
import RecordsDeleteCard from '../cards/RecordsDeleteCard.vue';

const props = defineProps<{
    incomingModel?: ResearchModel
    existingModels: ResearchModel[]
    projectId?: string,
    dependencies:{key:string,value:number,columns:string[]}[]
    relatedModelRecordsCounts:Record<string, number>,
    totalRecords:number
}>()

</script>