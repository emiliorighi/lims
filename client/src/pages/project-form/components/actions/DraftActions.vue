<template>
    <div class="row justify-space-between align-end">
        <div class="flex lg6 md6">
            <div class="row">
                <div class="flex">
                    <UploadDraftProject />
                </div>
                <div class="flex">
                    <UploadProject />
                </div>
            </div>
        </div>
        <div class="flex lg6 md6">
            <div class="row justify-end">
                <div class="flex">
                    <SaveDraftProject />
                </div>
                <div class="flex">
                    <DownloadYAML />
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import UploadProject from './components/UploadProject.vue'
import SaveDraftProject from './components/SaveDraftProject.vue';
import DownloadYAML from './components/DownloadYAMLProject.vue';
import UploadDraftProject from './components/UploadDraftProject.vue';

</script>