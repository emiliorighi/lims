<template>
    <VaLayout :top="{ fixed: true, order: 1 }"
        :left="{ fixed: true, absolute: breakpoints.smDown, order: 2, overlay: breakpoints.smDown && isSidebarVisible }"
        @left-overlay-click="isSidebarVisible = false">
        <template #top>
            <VaNavbar>
                <template #left>
                    <VaButton size="large" preset="secondary" :icon="isSidebarVisible ? 'menu_open' : 'menu'"
                        @click="isSidebarVisible = !isSidebarVisible" />
                    <VaBreadcrumbs class="va-title" color="primary">
                        <VaBreadcrumbsItem :to="bc.path" v-for="bc in breadcrumbs" :label="bc.name" />
                    </VaBreadcrumbs>
                </template>
                <template #right>
                    <VaButtonDropdown :closeOnContentClick="false" stickToEdges size="large" style="margin-right: 5px;"
                        color="secondary" preset="plain" icon="settings">
                        <ThemeColorSwitch />
                    </VaButtonDropdown>
                    <VaButtonDropdown style="margin-right: 5px;" :closeOnContentClick="false" stickToEdges size="large"
                        color="primary" preset="plain" icon="person"></VaButtonDropdown>
                    <!-- <VaIcon size="large" name="github" href="#"></VaIcon> -->
                </template>
            </VaNavbar>
            <VaDivider style="margin: 0" />
        </template>

        <template #left>
            <VaSidebar v-model="isSidebarVisible">
                <VaSidebarItem :active="isRouteActive(name)"  v-for="{ icon, title, name } in menu" :key="icon" :to="{name:name}">
                    <VaSidebarItemContent>
                        <VaIcon :name="icon" />
                        <VaSidebarItemTitle>
                            {{ title }}
                        </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                </VaSidebarItem>
            </VaSidebar>
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
import ThemeColorSwitch from '../components/navbar/components/ThemeColorSwitch.vue'


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

const menu = [
    { "icon": "dashboard", "title": "Dashboard", name:'home' },
    { "icon": "folder", "title": "Projects", name:'projects' },
    { "icon": "edit", "title": "Project Form" ,name:'project-form'},
    // { "icon": "drafts", "title": "Draft Projects",name:'projects' },
//     { "icon": "fa-vial", "title": "Samples" },
//     { "icon": "fa-dna", "title": "Experiments" }
]


function isRouteActive(name:string) {
    return name === useRoute().name || useRoute().fullPath.includes(name)
}

const breadcrumbs = computed(() => {
    const pathArray = route.path.split('/').filter(Boolean);
    const breadcrumbArray = [];
    let accumulatedPath = '';

    for (let i = 0; i < pathArray.length; i++) {
        accumulatedPath += '/' + pathArray[i];

        // Check if we are at a dynamic segment and replace it with actual value
        const matchedRoute = router.getRoutes().find(r => {
            const pathSegments = r.path.split('/').filter(Boolean);
            if (pathSegments.length === pathArray.length) {
                let isMatch = true;
                for (let j = 0; j <= i; j++) {
                    if (pathSegments[j].startsWith(':')) continue; // Ignore dynamic segments
                    if (pathSegments[j] !== pathArray[j]) {
                        isMatch = false;
                        break;
                    }
                }
                return isMatch;
            }
            return false;
        });

        if (matchedRoute) {
            const name = pathArray[i]
            breadcrumbArray.push({
                name,
                path: accumulatedPath,
            });
        }
    }

    return breadcrumbArray;
});

</script>
