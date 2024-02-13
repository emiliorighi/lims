<template>
    <div>
        <h1 class="va-h1">
            {{ schemaStore.schema.project_id }}
        </h1>
        <p> <b>Name:</b> {{ schemaStore.schema.name }}</p>
        <p> <b>Version:</b> {{ schemaStore.schema.version }}</p>
        <p v-if="schemaStore.schema.description"> <b>Description:</b> {{ schemaStore.schema.description }}</p>
        <va-tabs grow v-model="tab">
            <template #tabs>
                <va-tab v-for="t in ['samples', 'experiments']" :key="t" :name="t">
                    {{ t }}
                </va-tab>
            </template>
        </va-tabs>
        <va-divider />
        <router-view v-if="schemaStore.schema.project_id"></router-view>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref, watchEffect } from 'vue';
import { useSchemaStore } from '../../stores/schemas-store';
import { useRouter } from 'vue-router';
import ProjectService from '../../services/clients/ProjectService';

const schemaStore = useSchemaStore()
const router = useRouter()
const props = defineProps<{
    projectId: string
}>()

const tab = ref('samples')
onMounted(async () => {
    const { data } = await ProjectService.getProject(props.projectId)
    schemaStore.schema = { ...data }
})

watchEffect(() => {
    router.push({ name: tab.value })
})

</script>