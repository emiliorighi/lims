<template>
    <VaSidebar animated="left" v-model="isSidebarVisible" :minimized="minimized" minimized-width="64px">
        <div v-if="gStore.userName && !minimized" class="row align-center nav-h">
            <VaAvatar class="flex" color="info">
                {{ gStore.userName.charAt(0) }}
            </VaAvatar>
            <h5 class="va-h5 flex">{{ gStore.userName }}</h5>
        </div>
        <VaDivider style="margin: 0" />
        <VaSidebarItem :active="isRouteActive(name)" v-for="{ icon, title, name } in menu" :key="icon"
            :to="{ name: name }">
            <VaSidebarItemContent>
                <VaIcon :name="icon" />
                <VaSidebarItemTitle>
                    {{ title }}
                </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
    </VaSidebar>
</template>
<script setup lang="ts">
import { useRoute } from 'vue-router'

const props = defineProps<{
    minimized: boolean
    isSidebarVisible: boolean
}>()
export interface INavigationRoute {
    name: string
    displayName: string
    meta: { icon: string }
    children?: INavigationRoute[]
}

const route = useRoute()



const menu = [
    { icon: "dashboard", title: "Dashboard", name: 'home' },
    { icon: "folder", title: "Projects", name: 'projects' },
    { icon: "edit", title: "Project Form", name: 'project-form' },
    { icon: "account_circle", title: "Account", name: 'project-form' },

]


function isRouteActive(name: string) {
    return name === route.name || route.fullPath.includes(name)
}

</script>