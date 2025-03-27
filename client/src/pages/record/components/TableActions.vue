<template>
    <div class="row justify-space-between align-center">
        <div class="flex">
            <div class="row align-center">
                <div class="flex">
                    <h2 class="va-h6">
                        Results
                    </h2>
                </div>
                <div class="flex">
                    <VaChip outline color="textPrimary">
                        {{ total }}
                    </VaChip>
                </div>
            </div>
        </div>
        <div class="flex">
            <div class="row">
                <div class="flex">
                    <VaButton @click="recordStore.showReportModal = !recordStore.showReportModal" color="textPrimary"
                        preset="secondary" icon="fa-file-export" />
                </div>
                <div class="flex">
                    <VaButton @click="recordStore.showChartModal = !recordStore.showChartModal" color="textPrimary"
                        preset="secondary" icon="fa-chart-simple" />
                </div>
            </div>
        </div>
    </div>

</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useRecordStore } from '../../../stores/record-store';


const recordStore = useRecordStore()

const total = computed(() => recordStore.total)

</script>