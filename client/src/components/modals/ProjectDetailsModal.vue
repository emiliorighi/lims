<template>
    <VaModal max-height="500px" fixed-layout v-model="schemaStore.showSchema">
        <template #header>
            <div class="row align-center justify-space-between">
                <h3 class=" flex va-h3">
                    {{ schemaStore.schema.project_id }}
                </h3>
                <VaIcon color="primary" size="large" class="flex" name="folder" />

            </div>
        </template>
        <VaDivider />
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <MetadataTree :metadata="Object.entries(schemaStore.schema)" />
            </div>
        </div>
    </VaModal>
</template>
<script setup lang="ts">
import { useSchemaStore } from '../../stores/schemas-store';
import MetadataTree from '../ui/MetadataTree.vue';

const schemaStore = useSchemaStore()

</script>