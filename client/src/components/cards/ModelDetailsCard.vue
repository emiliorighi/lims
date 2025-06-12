<template>
    <VaCard outlined squared color="backgroundElement">
        <VaCardContent>
            <div class="row align-center">
                <div class="flex">
                    <h3 class="va-h6">
                        {{ title }}
                    </h3>
                    <p class="va-text-secondary">{{
                        model.description ? model.description : 'No description available' }}</p>
                </div>
                <div v-if="model.reference_model" class="flex">
                    <VaChip color="backgroundPrimary" size="small" icon="fa-link">{{
                        model.reference_model }}</VaChip>
                </div>
                <div class="flex" v-if="model.inherit_reference_id">
                    <VaChip size="small" color="warning">
                        Inherits IDs from {{ model.reference_model }}
                    </VaChip>
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <p> <strong>ID Fields: </strong></p>
            <div style="padding-left: 6px;" class="row">
                <div class="flex lg12 md12 sm12">
                    {{ model.id_format.join(', ') }}
                </div>
            </div>
        </VaCardContent>
        <VaCardContent>
            <p> <strong>Fields: </strong></p>
            <div style="padding-left: 6px;" v-for="field in model.fields" class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <p><strong>{{ field.key }}</strong></p>
                    <ul style="padding-left: 6px;">
                        <li>
                            Type: <span>{{ field.type }}</span>
                        </li>
                        <li v-if="field.description">
                            Description: <span>{{ field.required }}</span>
                        </li>
                        <li>
                            Required: <span>{{ field.required }}</span>
                        </li>
                        <li v-if="field.type === 'select'">
                            Multiple Choice: <span>{{ !!field.multi }}</span>
                        </li>
                        <li v-if="field.choices">
                            Options: <span>{{ field.choices.join(', ') }}</span>
                        </li>
                        <li v-if="field.regex">
                            Regex: <span>{{ field.regex }}</span>
                        </li>
                    </ul>
                </div>
            </div>
        </VaCardContent>
    </VaCard>

</template>
<script setup lang="ts">
import { ResearchModel } from '../../data/types';

const props = defineProps<{
    model: ResearchModel
    title: string
}>()

</script>