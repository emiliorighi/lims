<template>
    <div class="row justify-space-between align-end">
        <div class="flex">
            <h1 style="display: inline;" class="va-h1 pt-0">{{ schemaStore.schema.name }}</h1>
            <span style="margin-left: 3px;" class="va-text-secondary">{{ schemaStore.schema.version }}</span>
        </div>
        <div class="flex">
            <DownloadYAMLProject :project="schemaStore.schema" />
        </div>
    </div>
    <VaCard>
        <VaCardContent style="padding: 0;padding-top: 5px;">
            <VaTabs v-if="validTabs.length" v-model="tab">
                <template #tabs>
                    <VaTab v-for="(tab, index) in validTabs" :name="tab.name" :key="index" :label="tab.label"
                        :icon="tab.icon">
                        <!-- <VaButton block preset="secondary" border-color="primary" :icon="tab.icon">{{ tab.label }}</VaButton> -->
                    </VaTab>
                </template>
            </VaTabs>

        </VaCardContent>
        <VaDivider style="margin: 0;" />

        <VaCardContent>

            <router-view v-if="showProject"></router-view>

        </VaCardContent>
    </VaCard>
    <!-- <div class="row">
        <div class="flex lg6 md8 sm12 xs12">
            <VaTabs v-if="validTabs.length" v-model="tab">
                <template #tabs>
                    <VaTab v-for="(tab, index) in validTabs" :name="tab.name" :key="index" :label="tab.label"
                        :icon="tab.icon">
                    </VaTab>
                </template>
</VaTabs>
<VaButtonToggle v-if="validTabs.length" v-model="tab" preset="secondary" border-color="primary" :options="validTabs"
    valueBy="name" trackBy="name" textBy="label" />
</div>
<div class="flex"></div>
</div> -->




    <!-- <div class="row justify-space-between">
        <div class="flex">

        </div>
        <div class="flex">
        </div>
    </div> -->

    <!-- <VaTabs v-if="validTabs.length" v-model="tab">
        <template #tabs>
            <VaTab v-for="(tab, index) in validTabs" :name="tab.name" :key="index" :label="tab.label" :icon="tab.icon">
            </VaTab>
        </template>
</VaTabs> -->
    <!-- <VaDivider style="margin:0" /> -->
    <!-- <VaCard>
        <VaCardContent>
            <router-view v-if="showProject"></router-view>

        </VaCardContent>
    </VaCard> -->





    <!-- <VaDivider style="margin-top:0" /> -->


</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import ProjectService from '../../services/clients/ProjectService';
import { useRoute, useRouter } from 'vue-router';
import DownloadYAMLProject from '../../components/buttons/DownloadYAMLProject.vue';

const router = useRouter()
const route = useRoute()
const schemaStore = useSchemaStore()
const props = defineProps<{
    projectId: string
}>()


const showProject = computed(() => {
    return !!schemaStore.schema.project_id
})


const tab = ref('project')


watch(() => tab.value, () => {
    if (route.name && route.name !== tab.value) {
        const t = tabs.find(({ name }) => name === tab.value)
        if (t) {
            router.push(t.to)
        }
    }
})

onMounted(async () => {
    if (!schemaStore.schema.project_id) await getProject()

    if (!schemaStore.schema.experiment.id_format.length) {
        validTabs.value = [...tabs.filter(({ label }) => label !== 'Experiments')]
    } else {
        validTabs.value = [...tabs]
    }
    if (route.name !== tab.value) tab.value = route.name as string
})

const tabs = [
    {
        label: 'Overview',
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
    }
]

const validTabs = ref<Record<string, any>[]>([])

async function getProject() {
    try {
        const { data } = await ProjectService.getProject(props.projectId)
        schemaStore.schema = { ...data }
    } catch (error) {
        console.error(error)
    }
}


// function pushRoute(n: string) {
//     const t = tabs.find(({ name }) => name === n)
//     if (t) {
//         value.value = t.name
//         router.push(t.to)
//     }
// }
</script>