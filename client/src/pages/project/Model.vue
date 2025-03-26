<template>
    <div v-if="currentModel">
        <div class="row">
            <div class="flex">
                <h1 class="va-h1 va-text-capitalize">{{ modelName }}</h1>
                <p v-if="currentModel.description" class="va-text-secondary">
                    {{ currentModel.description }}
                </p>
            </div>
        </div>
        <div class="row justify-space-between">
            <div class="flex">
                <VaButtonGroup>
                    <VaButton color="textPrimary" :preset="view === opt.value ? undefined : 'primary'"
                        @click="view = opt.value" :key="opt.value" v-for="opt in options">
                        {{ opt.label }}
                    </VaButton>
                </VaButtonGroup>
            </div>
            <div class="flex">
                <VaButton @click="handleItemCreation" color="textPrimary" icon="fa-plus">
                    New {{ currentOption?.btn }}
                </VaButton>
            </div>
        </div>
        <Records v-if="view === 'records'" :model="currentModel" :project-id="projectId" />
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import Records from '../record/Records.vue';
import { useSchemaStore } from '../../stores/schema-store';
import { useRecordStore } from '../../stores/record-store';
import RecordForm from '../../components/record/RecordForm.vue';
import { useForm, useToast } from 'vuestic-ui';
import AuthService from '../../services/clients/AuthService';
import { AxiosError } from 'axios';

type ViewType = 'records' | 'links' | 'protocols'


const schemaStore = useSchemaStore()
const { validate } = useForm('recordForm')
const { init } = useToast()
const props = defineProps<{
    projectId: string,
    modelName: string
}>()
const view = ref<ViewType>('records')

const recordStore = useRecordStore()
const currentOption = computed(() => options.find(({ value }) => value === view.value))
const currentModel = computed(() => schemaStore.schema?.models.find(m => m.name === props.modelName))

const protocols = ref<Record<string, any>[]>([])
const links = ref<Record<string, any>[]>([])

// onMounted(() => )


const options: { label: string, value: ViewType, btn: string }[] = [
    { btn: 'Record', label: 'Records', value: 'records' },
    { btn: 'Protocol', label: 'Protocols', value: 'protocols' },
    { btn: 'Link', label: 'Links', value: 'links' }
]

function handleItemCreation() {
    if (!currentOption.value) return
    if (currentOption.value.value === 'records') recordStore.showRecordForm = !recordStore.showRecordForm
}

</script>