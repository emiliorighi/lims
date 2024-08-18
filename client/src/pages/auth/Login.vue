<template>
  <div class="row justify-center align-center">
    <div class="flex lg6 md8 sm12 xs12">
      <h1 class="va-h1">Login</h1>
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
</template>
<script setup lang="ts">
import { useGlobalStore } from '../../stores/global-store'
import { computed, ref } from 'vue'
import { VaCard, VaCardContent, VaInnerLoading } from 'vuestic-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
const GlobalStore = useGlobalStore()

const inputType = ref('password')
const isLoading = ref(false)

async function handleSubmit() {
  isLoading.value = true
  await GlobalStore.loginUser()
  if (GlobalStore.isAuthenticated) router.push({ name: 'projects' })
}

const name = computed({
  get() {
    return GlobalStore.userForm.name
  },
  set(v) {
    GlobalStore.userForm.name = v
  }
})

const password = computed({
  get() {
    return GlobalStore.userForm.password
  },
  set(v) {
    GlobalStore.userForm.password = v
  }
})
</script>
