<template>
    <VaMenu>
        <template #anchor>
            <VaButton color="textPrimary" preset="secondary" icon="more_horiz">
            </VaButton>
        </template>
        <VaMenuItem icon="fa-edit" @selected="emits('edit', record)" v-if="!disabledEdit">
            Edit
        </VaMenuItem>
        <VaMenuItem icon="fa-close" @selected="emits('delete', record)">
            Remove
        </VaMenuItem>
    </VaMenu>
</template>
<script setup lang="ts">
import { ResearchRecord } from '../../data/types';

const props = defineProps<{
    record: ResearchRecord
    disabledEdit: boolean,
}>()

const emits = defineEmits(['delete', 'edit'])

</script>