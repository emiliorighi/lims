<template>
    <div>
        <h1 class="va-h1 mb-2">
            {{ projectId }}
        </h1>
        <VaTabs @update:modelValue="pushRoute" v-model="value">
            <template #tabs>
                <VaTab v-for="tab in validTabs" :name="tab.name" :key="tab.label" :label="tab.label" :icon="tab.icon">
                </VaTab>
            </template>
        </VaTabs>
        <VaDivider style="margin-top:0" />
        <router-view v-if="showProject"></router-view>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import ProjectService from '../../services/clients/ProjectService';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter()
const route = useRoute()
const schemaStore = useSchemaStore()
const props = defineProps<{
    projectId: string
}>()


const showProject = computed(() => {
    return !!schemaStore.schema.project_id
})

watch(() => route.name, () => {
    if (route.name && route.name !== value.value) {
        const t = tabs.find(({ name }) => route.name === name)
        if (t) value.value = t.name
    }
})

onMounted(() => {
    if (route.name) value.value = route.name as string
})

const tabs = [
    {
        label: 'Details',
        icon: 'info',
        to: { name: 'project', params: { projectId: props.projectId } },
        name: 'project'
    },
    {
        label: 'Samples',
        icon: 'fa-vial',
        to: { name: 'samples' },
        name: 'samples'
    },
    {
        label: 'Experiments',
        icon: 'fa-dna',
        to: { name: 'experiments' },
        name: 'experiments'
    },
    {
        label: 'Upload',
        icon: 'upload',
        to: { name: 'upload' },
        name: 'upload'
    },
    {
        label: 'Statistics',
        icon: 'query_stats',
        to: { name: 'statistics' },
        name: 'statistics'
    },
]

const value = ref('')

const validTabs = computed(() => {
    if (schemaStore.schema.experiment.id_format.length) {
        return [...tabs]
    }
    return tabs.filter(({ label }) => label !== 'Experiments')
})
onMounted(async () => {
    if (!schemaStore.schema.project_id) await getProject()
})

async function getProject() {
    try {
        const { data } = await ProjectService.getProject(props.projectId)
        schemaStore.schema = { ...data }
    } catch (error) {
        console.error(error)
    }
}


function pushRoute(n: string) {
    const t = tabs.find(({ name }) => name === n)
    if (t) router.push(t.to)
}
</script>