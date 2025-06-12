<template>
    <VaModal v-model="gStore.showLoginModal" no-esc-dismiss no-dismiss no-outside-dismiss hide-default-actions title="Login">
        <VaForm @submit="login" ref="loginForm">
        <div class="layout va-gutter-5">
            <div class="row">
                <div class="flex">
                    <h1 class="va-h2" style="text-align: center;">
                        Login
                    </h1>
                    <p class="va-text-secondary">
                        Please login to continue
                    </p>
                </div>
            </div>
            <div class="row">
                <div class="flex lg6 md6 sm12 xs12">
                    <VaInput v-model="username" label="Username" placeholder="Username" :rules="[rules.required]" />

                </div>
                <div class="flex lg6 md6 sm12 xs12">
                    <VaInput v-model="password" label="Password" type="password" placeholder="Password" :rules="[rules.required]" />
                </div>
            </div>
            <div class="row">
                <div class="flex">
                    <VaButton type="submit" block >Login</VaButton>
                </div>
            </div>
        </div>
    </VaForm>
    </VaModal>
</template>

<script setup lang="ts">
import { useForm } from 'vuestic-ui/web-components';
import { useGlobalStore } from '../../stores/global-store';
import { ref } from 'vue';

const gStore = useGlobalStore()

const rules = {
    required: (value: string) => !!value || 'Required',
}

const {validate} = useForm('loginForm')
const username = ref('')
const password = ref('')

const login = async () => {
    if(!validate()) return
    try {
        await gStore.login(username.value, password.value)
        gStore.toggleLoginModal()
    } catch (error) {
        console.error(error)
        gStore.toast({ message: 'Bad user or password', color: 'danger' })
    }
}
</script>