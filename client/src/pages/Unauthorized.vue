<template>
    <div class="layout va-gutter-5">
        <div class="row justify-center align-center">
            <div class="flex">
                <h1 class="va-h1">
                    Your are not authorized!
                </h1>
                <p>
                    You are not authorized to access this page.
                </p>
            </div>
        </div>
        <div class="row justify-center align-center">
            <div class="flex">
                <VaButton @click="goToHome" preset="primary">
                    Go to Home
                </VaButton>
            </div>
            <div class="flex">
                <VaButton @click="goToLogin" preset="secondary">
                    Go to Login
                </VaButton>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToHome = () => {
    router.push('/')
}

const goToLogin = () => {
    router.push('/login')
}
</script>
<style scoped>
.layout {
    height: 100vh;
}
</style>