<template>
    <VaSelect :disabled="noRefenceItems" @update:search="getRecords" searchable searchPlaceholderText="Type to search"
        noOptionsText="No records found, refine your search criteria" v-model="recordStore.recordForm.reference_id"
        :options="referenceRecords" clearable :rules="[(v: any) => !!v || 'Field is mandatory']"
        :loading="searchLoading" textBy="item_id" trackBy="item_id" valueBy="item_id" />

</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRecordStore } from '../../stores/record-store';
import RecordService from '../../services/clients/RecordService';
import { useToast } from 'vuestic-ui/web-components';
import { useModelStore } from '../../stores/model-store';

const props = defineProps<{
    projectId: string
    modelName: string,
}>()

const { init } = useToast()
const recordStore = useRecordStore()
const modelStore = useModelStore()
const searchLoading = ref(false)
const referenceRecords = ref<Record<string, any>[]>([])
const referenceTotal = ref(0)
const noRefenceItems = ref(false)
const refModelName = computed(() => modelStore.refModel?.name)

onMounted(async () => {
    await getRecords("")
})

async function getRecords(filter: string) {
    if (!refModelName.value) return
    try {
        searchLoading.value = true
        const { data } = await RecordService.getItems(props.projectId, refModelName.value, { filter })
        referenceRecords.value = [...data.data]
        referenceTotal.value = data.total
    } catch (err) {
        console.error(err)
        init({ message: 'Error fetching records, check the logs', color: 'danger' })
    } finally {
        searchLoading.value = false
    }
}


</script>
