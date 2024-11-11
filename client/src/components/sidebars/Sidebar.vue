<template>
    <VaSidebar v-model="globalStore.isSidebarVisible">
        <VaSidebarItem :active="isRouteActive('home')" :to="{ name: 'home' }">
            <VaSidebarItemContent>
                <VaIcon name="dashboard" />
                <VaSidebarItemTitle>
                    Dashboard
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem :active="isRouteActive('projects')" :to="{ name: 'projects' }">
            <VaSidebarItemContent>
                <VaIcon name="folder" />
                <VaSidebarItemTitle>
                    Projects
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem v-if="isAdmin" :active="isRouteActive(name)" v-for="{ icon, title, name } in adminMenu"
            :key="icon" :to="{ name: name }">
            <VaSidebarItemContent>
                <VaIcon :name="icon" />
                <VaSidebarItemTitle>
                    {{ title }}
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
        <VaSidebarItem :active="isRouteActive('docs')" :to="{ name: 'docs' }">
            <VaSidebarItemContent>
                <VaIcon name="quiz" />
                <VaSidebarItemTitle>
                    Documentation
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
            <VaSidebarItemContent @click="$router.push({ name: 'login' })">
                <VaIcon name="login" />
                <VaSidebarItemTitle>
                    Login
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
    </VaSidebar>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGlobalStore } from "../../stores/global-store"

const globalStore = useGlobalStore()

const isAdmin = computed(() => {
    return globalStore.user.role === 'admin'
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
    await globalStore.logout()
    router.push({ name: 'home' })
}

const adminMenu = [
    { icon: "edit", title: "Project Form", name: 'project-form' },
    { icon: "group", title: "Users", name: 'users' },
]
</script>