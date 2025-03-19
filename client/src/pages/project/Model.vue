<template>
    <div v-if="currentModel">
        <div class="row align-end justify-space-between">
            <div class="flex">
                <h1 class="va-h1 va-text-capitalize">{{ modelName }}</h1>
                <p v-if="currentModel.description" class="va-text-secondary">
                    {{ currentModel.description }}
                </p>
            </div>
            <div class="flex">
                <VaButtonToggle toggle-color="textPrimary" color="backgroundElement" v-model="view" :options="options">
                </VaButtonToggle>
            </div>
        </div>
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <VaCard>
                    <VaCardContent v-if="view === 'records'">
                        <Records :model="currentModel" :project-id="projectId" />
                    </VaCardContent>
                    <VaCardContent v-else-if="view === 'protocols'">

                    </VaCardContent>
                    <VaCardContent v-else>

                    </VaCardContent>
                </VaCard>
            </div>
        </div>
        <VaModal v-model="recordStore.showRecordForm" noDismiss hideDefaultActions close-button>
            <template #header>
                <h3 class="va-h3">
                    {{ formInfo.title }}
                </h3>
                <p class="va-text-secondary">{{ formInfo.description }}</p>
            </template>
            <div class="layout fluid va-gutter-5">
                <VaForm ref="recordForm">
                    <RecordForm :project-id="projectId" :model="currentModel"
                        :referenceModel="currentModel.reference_model" />
                </VaForm>
            </div>
            <template #footer>
                <div class="row justify-space-between">
                    <div class="flex">
                        <VaButton @click="recordStore.showRecordForm = !recordStore.showRecordForm" color="textPrimary"
                            preset="primary">Close Form</VaButton>
                    </div>
                    <div class="flex">
                        <VaButton @click="handleSubmit" color="textPrimary">Submit</VaButton>
                    </div>
                </div>
            </template>
        </VaModal>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import Records from './components/Records.vue';
import { useSchemaStore } from '../../stores/schema-store';
import { useRecordStore } from '../../stores/record-store';
import RecordForm from '../../components/record/RecordForm.vue';
import { useForm, useToast } from 'vuestic-ui';
import AuthService from '../../services/clients/AuthService';
import { AxiosError } from 'axios';

const schemaStore = useSchemaStore()
const { validate } = useForm('recordForm')
const { init } = useToast()
const props = defineProps<{
    projectId: string,
    modelName: string
}>()
const loading = ref(false)
const recordStore = useRecordStore()
const idToUpdate = computed(() => recordStore.idToUpdate)
const formInfo = computed(() => idToUpdate.value ? {
    title: 'Update Record',
    description: `Update ${idToUpdate.value}`
} : {
    title: 'Create Record',
    description: `Create a new ${props.modelName}`
})
const currentModel = computed(() => schemaStore.schema?.models.find(m => m.name === props.modelName))

onMounted(async () => {

})

const protocols = ref<Record<string, any>[]>([])
const links = ref<Record<string, any>[]>([])

async function handleSubmit() {
    if (!validate()) {
        init({ message: 'Fill the required fields', color: 'danger' })
        return
    }
    const filteredEntries = Object.entries(recordStore.recordForm).filter(
        ([, v]) => v === 0 || (v && !(Array.isArray(v) && v.length === 0))
    );
    let success = false
    try {
        loading.value = true
        if (idToUpdate.value) {
            const { data } = await AuthService.updateRecord(props.projectId, props.modelName, idToUpdate.value, Object.fromEntries(filteredEntries))
            init({ message: 'Record correctly updated', color: 'success' })
        } else {
            const { data } = await AuthService.createRecord(props.projectId, props.modelName, Object.fromEntries(filteredEntries))
            init({ message: 'Record correctly created', color: 'success' })
        }

        success = true
    } catch (err) {
        success = false
        const axiosError = err as AxiosError
        const respData = axiosError.response?.data as { message: string }
        init({ message: respData.message, color: 'danger', duration: 10000 })
    }
    finally {
        loading.value = false
        if (!success) return
        recordStore.resetForm()
        recordStore.showRecordForm = false
        await recordStore.fetchRecords(props.projectId, props.modelName)
    }
}
// onMounted(() => )

const view = ref('records')

const options = [
    { label: 'Records', value: 'records' },
    { label: 'Protocols', value: 'protocols' },
    { label: 'Links', value: 'links' }
]


</script>