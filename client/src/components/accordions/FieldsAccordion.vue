<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaAccordion stateful class="max-w-sm">
                <VaCollapse v-for="field in fields" :key="field.key">
                    <template #header-content>
                        <div class="row">
                            <div class="flex">
                                <h3 class="va h6">
                                    {{ field.key }}
                                </h3>
                            </div>
                            <div class="flex">
                                <VaChip color="backgroundElement" size="small">{{ field.type }}</VaChip>
                            </div>
                            <div v-if="idFormat.includes(field.key)" class="flex">
                                <VaChip color="warning" size="small">ID Field</VaChip>
                            </div>
                            <div v-if="field.required" class="flex">
                                <VaChip size="small" color="danger">Required</VaChip>
                            </div>
                        </div>
                    </template>
                    <template #content>
                        <div class="row">
                            <div class="flex lg12 md12 sm12 xs12 va-text-secondary">
                                <span class="va-text-bold">Description: </span> <span>{{
                                    field.description ?? 'No Description available' }}</span>
                                <VaButton icon="fa-edit" preset="secondary"></VaButton>
                            </div>
                            <div v-if="field.multi" class="flex lg12 md12 sm12 xs12">
                                <p class="va-text-secondary"><span class="va-text-bold">Multiple Choice: </span>
                                    {{ field.multi }}</p>
                            </div>
                            <div v-if="field.choices?.length" class="flex lg12 md12 sm12 xs12">
                                <p class="va-text-secondary"><span class="va-text-bold">Choices: </span>
                                </p>
                                <p class="va-text-secondary">
                                    {{ field.choices.join(', ') }}
                                </p>
                            </div>
                            <div v-if="field.regex" class="flex lg12 md12 sm12 xs12">
                                <p class="va-text-secondary"><span class="va-text-bold">Regex Rule: </span>
                                    {{ field.regex }}</p>
                            </div>
                        </div>
                    </template>
                </VaCollapse>
            </VaAccordion>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ResearchFilter } from '../../data/types';

const props = defineProps<{
    fields: ResearchFilter[]
    idFormat: string[]
}>()


</script>