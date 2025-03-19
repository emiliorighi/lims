<template>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <h3 class="va-h6">
                {{ title }}
            </h3>
            <VaCard outlined squared color="backgroundElement">
                <VaCardContent v-if="model.description">
                    <p class="va-text-secondary">{{
                        model.description }}</p>
                </VaCardContent>
                <VaCardContent v-if="model.reference_model">
                    <p> <strong>Reference Model:</strong></p>
                    <p>
                        {{ model.reference_model }}
                    </p>
                </VaCardContent>
                <VaCardContent>
                    <p> <strong>ID Format: </strong></p>
                    <div style="padding-left: 6px;" class="row">
                        <div class="flex lg12 md12 sm12">
                            {{ model.id_format.join('_') }}
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
        </div>
    </div>
</template>
<script setup lang="ts">
import { ReseachModel } from '../../data/types';

const props = defineProps<{
    model: ReseachModel
    title: string
}>()

</script>