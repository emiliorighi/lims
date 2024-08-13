<template>
    <VaBreadcrumbs class="va-title" color="primary">
        <VaBreadcrumbsItem :to="bc.path" v-for="bc in breadcrumbs" :label="bc.name" />
    </VaBreadcrumbs>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const breadcrumbs = computed(() => {
    const pathArray = route.path.split('/').filter(Boolean);
    const breadcrumbArray = [] as { name: string, path: string }[];
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
