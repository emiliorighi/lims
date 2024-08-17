<template>
    <VaModal max-height="500px" fixed-layout v-model="schemaStore.showSchema">
        <template #header>
            <Header :title="schemaStore.schema.project_id" icon="folder"/>
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
import Header from './common/Header.vue'

const schemaStore = useSchemaStore()

</script>