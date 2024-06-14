<template>
    <div>
        <h1 class="va-h1">Project form</h1>
        <p style="margin-bottom: 6px" class="va-text-secondary">Fill all the steps to create a new project, save it to
            draft at any moment</p>
        <DraftActions />
    </div>
</template>
<script setup lang="ts">
import DraftActions from './actions/DraftActions.vue'
</script>