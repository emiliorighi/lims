<template>
  <NewLayout></NewLayout>
</template>
<script setup lang="ts">
import NewLayout from './layouts/NewLayout.vue';
import ProjectLayout from './layouts/ProjectLayout.vue';
import AuthService from './services/clients/AuthService'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGlobalStore } from './stores/global-store'
import { AxiosError } from 'axios'
import { computed } from 'vue';
import { useRoute } from 'vue-router';


const gStore = useGlobalStore()

const router = useRouter()

const route = useRoute();
// const layoutKey = computed(() => route.meta.layout || 'default');
// const layout = computed(() => {
//   if (route.meta.layout === 'project') {
//     return ProjectLayout;
//   }
//   return NewLayout;
// });
onMounted(async () => {

  await checkUserisLoggedIn()

})

async function checkUserisLoggedIn() {
  try {
    const { data } = await AuthService.check()
    gStore.isAuthenticated = true
    gStore.userName = data.name
    gStore.userRole = data.role
    gStore.userProjects = [...data.projects]
  } catch (error) {

    const axiosError = error as AxiosError
    // Handle specific types of errors if necessary
    if (axiosError.response && axiosError.response.status === 401) {
      router.push({ name: 'login' })
    } else {
      console.error('An unexpected error occurred during authentication check.');
    }
  }
}

</script>
<style lang="scss">
@import 'scss/main.scss';

#app {
  font-family: 'Source Sans Pro', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

body {
  margin: 0;
}

.pt-0 {
  padding-top: 0;
}

.p-0 {
  padding: 0;
}

.p-6 {
  padding: 6px;
}

.va-dropdown__content.va-select-dropdown__content.va-dropdown__content-wrapper {
  z-index: 101 !important;
}

.nav-h {
  height: 85px;
}

.row-equal .flex {
  .va-card {
    height: 100%;
  }
}
</style>
