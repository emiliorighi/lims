<template>
  <div class="layout va-gutter-5">
    <div class="row justify-center align-center">
    <div class="flex">
      <h1 class="va-h1 mb-2">Login</h1>
      <VaCard>
        <VaCardContent>
          <VaInnerLoading :loading="isLoading">
            <VaForm tag="form">
              <VaInput v-model="name" class="mt-3" label="username"> </VaInput>
              <VaInput v-model="password" class="mt-3" label="password" :type="inputType">
                <template #appendInner>
                  <VaIcon :name="inputType === 'password' ? 'visibility' : 'visibility_off'"
                    @click="inputType === 'password' ? (inputType = 'text') : (inputType = 'password')" />
                </template>
              </VaInput>
              <VaButton @click="handleSubmit" :disabled="!name || !password" class="mt-3" type="submit">
                Login
              </VaButton>
            </VaForm>
          </VaInnerLoading>
        </VaCardContent>
      </VaCard>
    </div>
  </div>
  </div>

</template>
<script setup lang="ts">
import { useGlobalStore } from '../stores/global-store'
import { VaCard, VaCardContent, VaInnerLoading } from 'vuestic-ui'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()
const GlobalStore = useGlobalStore()

const name = ref('')
const password = ref('')
const inputType = ref('password')
const isLoading = ref(false)

async function handleSubmit() {
  isLoading.value = true
  await GlobalStore.login(name.value, password.value)
  if (GlobalStore.isAuthenticated) router.back()
}

</script>
<style scoped>
.layout {
    height: 100vh;
}
.mb-2 {
    margin-bottom: 2rem;
}
</style>
