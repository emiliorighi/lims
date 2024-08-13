<template>
    <div class="row">
        <VaSelect class="flex lg6 md6 sm12 xs12" :disabled="validOpts.length === 1" v-model="model" :options="validOpts"
            :messages="['The model in use']">
            <template #prependInner>
                <VaIcon style="margin-right: 5px;" :color="model === 'sample' ? 'success' : 'primary'"
                    :name="model === 'sample' ? 'fa-vial' : 'fa-dna'" />
            </template>
        </VaSelect>
        <VaSelect class="flex lg6 md6 sm12 xs12" v-model="behaviour" :messages="[`SKIP or UPDATE existing ${model}s`]"
            :options="['SKIP', 'UPDATE']" />
    </div>
    <div class="row">
        <div class="flex lg12 md12 sm12 xs12">
            <VaFileUpload dropzone style="z-index: 0" v-model="tsv" file-types=".tsv" type="single" undo
                :uploadButtonText="`Upload ${model}s`" />
        </div>
    </div>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import { useToast } from 'vuestic-ui/web-components';
import { computed, ref, watch } from 'vue';
import ProjectService from '../../services/clients/ProjectService';

const { init } = useToast()
const schemaStore = useSchemaStore()
const isLoading = ref(false)
const tsv = ref()
const behaviour = ref('SKIP')
const model = ref<'sample' | 'experiment'>('sample')

const emits = defineEmits(['onMapped', 'onModelChange'])

const validOpts = computed(() => {
    if (schemaStore.schema.experiment.id_format.length === 0) return ['sample']
    return ['sample', 'experiment']
})


watch(() => tsv.value, async () => {
    if (tsv.value) {
        await fetchHeaderMap(schemaStore.schema.project_id)
    }
})

watch(() => model.value, async () => {
    if (tsv.value) {
        await fetchHeaderMap(schemaStore.schema.project_id)
    }
    emits('onModelChange', model.value)
})


async function fetchHeaderMap(projectId: string) {
    try {
        isLoading.value = true
        const formData = new FormData()
        formData.append('tsv', tsv.value)
        formData.append('model', model.value)
        const { data } = await ProjectService.inferHeadersFromTSV(projectId, formData)
        emits('onMapped', [...data])

    } catch (error) {
        console.error(error)
        init({ message: 'Error mapping project..', color: 'danger', duration: 1500 })
    } finally {
        isLoading.value = false
    }

}

</script>
