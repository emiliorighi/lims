<template>
    <div>
        <h1 class="va-h1 mb-2">
            {{ projectId }}
        </h1>
        <va-tabs @update:modelValue="pushRoute" v-model="value">
            <template #tabs>
                <va-tab :name="tab.label" v-for="tab in validTabs" :key="tab.label" :label="tab.label" :icon="tab.icon">
                </va-tab>
            </template>
        </va-tabs>
        <VaDivider style="margin-top:0" />

        <!-- <div class="row">
            <div class="flex">
                <VaButton :to="{ name: 'samples', params: { projectId: projectId } }" icon="fa-vial" color="success">
                    Samples {{ lookupData.samples }}</VaButton>
            </div>
            <div class="flex">
                <VaButton :to="{ name: 'experiments', params: { projectId: projectId } }" icon="fa-dna">Experiments {{
                lookupData.experiments }}</VaButton>
            </div>
        </div> -->
        <router-view v-if="showProject"></router-view>
        <!-- <div v-if="showProject" class="row">
            <div class="flex lg4 md4 sm12 xs12">
                <VaCard>
                    <VaCardTitle>Project schema</VaCardTitle>
                    <ProjectOverviewCard :metadata="schemaStore.schema" />
                </VaCard>
            </div>
        </div> -->
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import ProjectService from '../../services/clients/ProjectService';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter()
const route = useRoute()
const schemaStore = useSchemaStore()
const props = defineProps<{
    projectId: string
}>()
const lookupData = ref({ samples: 0, experiments: 0 })

const value = ref('Details')

const showProject = computed(() => {
    return !!schemaStore.schema.project_id
})

const tabs = [
    {
        label: 'Details',
        icon: 'info',
    },
    {
        label: 'Samples',
        icon: 'fa-vial',
    },
    {
        label: 'Experiments',
        icon: 'fa-dna',
    },
    {
        label: 'Upload',
        icon: 'upload',
    },
    {
        label: 'Statistics',
        icon: 'query_stats',
    },
]

const validTabs = computed(() => {
    if (schemaStore.schema.experiment.id_format.length) {
        return [...tabs]
    }
    return tabs.filter(({ label }) => label !== 'Experiments')
})
onMounted(async () => {
    if (!schemaStore.schema.project_id) await getProject()
    const currentRoute = route.name
    if (currentRoute && currentRoute !== 'project') {
        value.value = capitalizeFirstChar(currentRoute.toString())
    }

})

function capitalizeFirstChar(str: string) {
    if (str.length === 0) return str; // Handle empty string
    const [first, ...rest] = str;
    return first.toUpperCase() + rest.join('');
}
async function getProject() {
    try {
        const { data } = await ProjectService.getProject(props.projectId)
        schemaStore.schema = { ...data }
    } catch (error) {
        console.error(error)
    }
}

// async function getData() {
//     try {
//         const response = await ProjectService.lookupProject(props.projectId)
//         const { samples, experiments } = response.data
//         lookupData.value = { samples, experiments }
//     } catch (error) {
//         console.error(error)
//     }
// }

function pushRoute(value: 'Details' | 'Samples' | 'Experiments' | 'Upload' | 'Statistics') {
    if (value === 'Details') {
        router.push({ name: 'project', params: { projectId: props.projectId } })
    } else if (value === 'Experiments') {
        router.push({ name: 'experiments', params: { projectId: props.projectId } })
    } else if (value === 'Samples') {
        router.push({ name: 'samples', params: { projectId: props.projectId } })
    } else if (value === 'Upload') {
        router.push({ name: 'upload', params: { projectId: props.projectId } })
    } else {
        router.push({ name: 'statistics', params: { projectId: props.projectId } })
    }
}
</script>