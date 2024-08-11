<template>
    <div class="row justify-space-between">
        <div class="flex lg4 md4 sm12 xs12">
            <VaCounter manual-input :rules="minRules" type="number" label="Min" v-model="range.min" />
        </div>
        <div class="flex lg4 md4 sm12 xs12">
            <VaCounter manual-input :rules="maxRules" type="number" label="Max" v-model="range.max" />
        </div>
        <div class="flex lg8 md8 sm12 xs12">
            <VaInput :rules="unitRules" label="Unit" v-model="range.unit" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Range } from './../../data/types';

const range = ref<Range>({
    min: 0,
    max: 0,
    unit: '',
});

const minRules = [
    (v: any) => typeof v === 'number' && !isNaN(v) || 'Value must be a number',
    (v: number) => v < range.value.max || 'Min must be less than Max',
];

const maxRules = [
    (v: any) => typeof v === 'number' && !isNaN(v) || 'Value must be a number',
    (v: number) => v > range.value.min || 'Max must be greater than Min',
];

const unitRules = [(v: string) => v.length > 0 || 'Unit is mandatory'];
</script>