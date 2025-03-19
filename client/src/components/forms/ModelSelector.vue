<template>
    <div class="row">
        <VaSelect class="flex lg6 md6 sm12 xs12" :disabled="validModels.length === 1" v-model="selectedModel"
            :options="validModels" :messages="['The model in use']">
            <template #prependInner>
                <VaIcon class="mr-1" :color="model === 'sample' ? 'success' : 'primary'" :name="modelIcon" />
            </template>
        </VaSelect>

        <VaSelect class="flex lg6 md6 sm12 xs12" v-model="selectedBehavoiur"
            :messages="[`SKIP or UPDATE existing ${model}s`]" :options="['SKIP', 'UPDATE']" />
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useSchemaStore } from '../../stores/schema-store';

const props = defineProps<{
    model: string,
    behaviour: string,
}>();

const selectedModel = computed({
    get() {
        return props.model
    },
    set(v) {
        emit('update:model', v)
    }
})

const selectedBehavoiur = computed({
    get() {
        return props.behaviour
    },
    set(v) {
        emit('update:behaviour', v)
    }
})
const emit = defineEmits(['update:model', 'update:behaviour']);

const schemaStore = useSchemaStore();

const validModels = computed(() => {
    if (schemaStore.schema.experiment.id_format.length === 0) return ['sample'];
    return ['sample', 'experiment'];
});

const modelIcon = computed(() => {
    return props.model === 'sample' ? 'fa-vial' : 'fa-dna';
});

</script>