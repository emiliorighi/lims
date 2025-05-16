<template>
    <div class="row">
        <div class="flex">
            <h2 class="va-h2">
                Resume
            </h2>
            <p>Review and submit the model</p>
        </div>
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <ModelDetailsCard :model="modelValue" :title="modelValue.name" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ResearchModel } from '../../../data/types'
import ModelDetailsCard from '../../cards/ModelDetailsCard.vue'

defineProps<{
    modelValue: ResearchModel,
}>()
</script> 