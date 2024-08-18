<template>
    <VaSidebar :minimized="isProjectView" v-model="globalStore.isSidebarVisible">
        <VaSidebarItem :active="isRouteActive(name)" v-for=" { icon, title, name }  in  menu " :key="icon"
            :to="{ name: name }">
            <VaSidebarItemContent>
                <VaIcon :name="icon" />
                <VaSidebarItemTitle>
                    {{ title }}
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem :active="isRouteActive('users')" v-if="globalStore.user.role === 'admin'"
            :to="{ name: 'users' }">
            <VaSidebarItemContent>
                <VaIcon name="group" />
                <VaSidebarItemTitle>
                    Users
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem href="https://github.com/emiliorighi/lims/issues/new" target="_blank">
            <VaSidebarItemContent>
                <VaIcon name="github" />
                <VaSidebarItemTitle>
                    Open Issue
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem v-if="globalStore.isAuthenticated">
            <VaSidebarItemContent @click="logout">
                <VaIcon name="logout" />
                <VaSidebarItemTitle>
                    Logout
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem v-else>
            <VaSidebarItemContent @click="logout">
                <VaIcon name="logout" />
                <VaSidebarItemTitle>
                    Logout
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
    </VaSidebar>
    <VaDivider vertical style="margin: 0;" />
    <VaSidebar hoverable minimized-width="64px" v-if="isProjectView" v-model="globalStore.isSidebarVisible">
        <VaSidebarItem :active="isSubRouteActive(m.name)" v-for=" m  in  projectMenu " :key="m.name" :to="m.to">
            <VaSidebarItemContent>
                <VaIcon :name="m.icon" />
                <VaSidebarItemTitle>
                    {{ m.label }}
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
    </VaSidebar>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGlobalStore } from "../../stores/global-store"
import { useSchemaStore } from "../../stores/schemas-store"

const schemaStore = useSchemaStore()
const globalStore = useGlobalStore()

const tabs = [
    {
        label: 'Summary',
        icon: 'summarize',
        to: { name: 'project' },
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


const projectMenu = computed(() => {
    const projectId = schemaStore.schema.project_id
    if (!projectId) return
    if (schemaStore.schema.experiment.id_format.length) {
        return tabs
    } return tabs.filter(t => t.name !== 'experiments')
})

const mainMenu = computed(() => {
    const isAdmin = globalStore.user.role === 'admin'
    
})

const isProjectView = computed(() => {
    return !!route.params.projectId
})

const route = useRoute()
const router = useRouter()

function isSubRouteActive(name: string) {
    return name === route.name
}

function isRouteActive(name: string) {
    return isSubRouteActive(name) || route.fullPath.includes(name)
}

async function logout() {
    await globalStore.logoutUser()
    router.push({ name: 'home' })
}

const menu = [
    { icon: "dashboard", title: "Dashboard", name: 'home' },
    { icon: "folder", title: "Projects", name: 'projects' },
    { icon: "edit", title: "Project Form", name: 'project-form' },
]

</script>