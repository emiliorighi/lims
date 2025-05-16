<template>
    <VaCard>
        <VaCardContent>
            <div class="row">
                <div class="flex">
                    <h2 class="va-h4">Attributes</h2>
                    <p class="va-text-secondary">
                        List of attributes used to define records
                    </p>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <div class="row">
                <div v-for="field in fields" :key="field.key" class="flex">
                    <VaDropdown stick-to-edges :close-on-content-click="false">
                        <template #anchor>
                            <VaBadge overlap color="warning"
                                :text="idFormat.includes(field.key) ? 'ID' : field.required ? 'Required' : undefined">
                                <VaChip :icon="getIcon(field.type)" color="backgroundElement">{{ field.key }}
                                </VaChip>
                            </VaBadge>
                        </template>
                        <VaDropdownContent>
                            <div class="layout va-gutter-3">
                                <div class="row">
                                    <div class="flex lg12 md12 sm12 xs12 va-text-secondary">
                                        {{
                                            field.description ? field.description : 'No Description available' }}

                                    </div>
                                    <div v-if="field.multi" class="flex lg12 md12 sm12 xs12">
                                        <p class="va-text-secondary"><span class="va-text-bold">Multiple Choice:
                                            </span>
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
                                        <p class="va-text-secondary"><span class="va-text-bold">Regex Rule:
                                            </span>
                                            {{ field.regex }}</p>
                                    </div>
                                </div>
                            </div>

                        </VaDropdownContent>
                    </VaDropdown>
                </div>
            </div>
        </VaCardContent>
    </VaCard>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useModelStore } from '../../stores/model-store';

const modelStore = useModelStore()
const fields = computed(() => modelStore.filters)
const idFormat = computed(() => modelStore.idFormat)

function getIcon(type: 'select' | 'date' | 'number' | 'text') {
    return type === 'select' ? 'fa-tag' : type === 'date' ? 'fa-calendar' : type === 'number' ? 'fa-hashtag' : 'fa-edit'

}

</script>