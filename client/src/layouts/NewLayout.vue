<template>
    <VaLayout :top="{ fixed: true, order: 1 }"
        :left="{ fixed: true, absolute: breakpoints.smDown, order: 2, overlay: breakpoints.smDown && isSidebarVisible }"
        @left-overlay-click="isSidebarVisible = false">
        <template #top>
            <NavBar />
            <VaDivider style="margin: 0" />
        </template>

        <template #left>
            <MainSidebar :isSidebarVisible="isSidebarVisible" :minimized="true" />
            <!-- <VaSidebar color="primary" hover-color="secondary">
                <VaSidebarItem v-for="icon in mainMenu" :key="icon">
                    <VaSidebarItemContent @click="isSidebarVisible = !isSidebarVisible">
                        <VaIcon :name="icon" />
                    </VaSidebarItemContent>
                </VaSidebarItem>
            </VaSidebar> -->
        </template>
        <template #content>
            <main>
                <div class="layout fluid va-gutter-5">
                    <router-view v-slot="{ Component }">
                        <Transition name="fade">
                            <component :is="Component" />
                        </Transition>
                    </router-view>
                </div>
            </main>
        </template>
    </VaLayout>
</template>

<script setup lang="ts">
import { computed, ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBreakpoint } from 'vuestic-ui'
import { useGlobalStore } from "../stores/global-store"
import NavBar from '../components/navbar/Navbar.vue'
import MainSidebar from '../components/sidebar/MainSidebar.vue'


const gStore = useGlobalStore()

export interface INavigationRoute {
    name: string
    displayName: string
    meta: { icon: string }
    children?: INavigationRoute[]
}
const breakpoints = useBreakpoint()

const route = useRoute()
const router = useRouter()

const isSidebarVisible = ref(breakpoints.mdUp)

watchEffect(() => {
    isSidebarVisible.value = breakpoints.smUp
})
</script>
