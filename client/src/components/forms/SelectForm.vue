<template>
    <div>
        <VaSelect label="Is Field Multiple Choice?" v-model="select.multi" :options="[true, false]" />
        <div class="row justify-center">
            <div v-for="(choice, index) in select.choices" :key="index" class="flex lg12 md12 sm12 xs12">
                <VaInput :label="`Choice #${index + 1}`" class="mt-2" :rules="choiceRules(index)"
                    v-model="select.choices[index]">
                    <template #appendInner>
                        <VaButton :disabled="index < 2" color="danger" size="small" icon="delete"
                            @click="removeChoice(index)" />
                    </template>
                </VaInput>
            </div>
            <VaButton class="mt-2" size="small" @click="addChoice" icon="add">New Choice</VaButton>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Select } from './../../data/types';

const select = ref<Select>({
    multi: false,
    choices: [''],
});


const emit = defineEmits(['update:value']);

function addChoice() {
    select.value.choices.push('');
}

function removeChoice(index: number) {
    select.value.choices.splice(index, 1);
}


const choiceRules = (index: number) => [
    (v: string) => v.length > 0 || 'Insert a valid value',
    (v: string) => select.value.choices.findIndex(c => c === v) === -1 || select.value.choices.find

]