<template>
    <div>
        <div class="row">
            <div class="flex lg12 md12 sm12 xs12">
                <h1 class="va-h1">
                    Model Creation
                </h1>
            </div>
        </div>
        <VaForm ref="modelForm">
            <div class="row">
                <div class="flex lg12 md12 sm12 xs12">
                    <VaCard :stripe="modelNames.includes(modelStore.modelForm.name)"
                        :stripe-color="modelNames.includes(modelStore.modelForm.name) ? 'danger' : undefined">
                        <VaCardContent>
                            <p v-if="modelNames.includes(modelStore.modelForm.name)" class="va-text-danger">This name
                                already exists,
                                change it</p>
                            <ModelInfo :description="modelStore.modelForm.description" :type="modelStore.modelForm.name"
                                @update-type="(v: string) => modelStore.modelForm.name = v"
                                @update-description="(v: string) => modelStore.modelForm.description = v" />
                        </VaCardContent>
                    </VaCard>
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaCard>
                                <VaCardContent>
                                    <ModelAttributes v-model:model-attributes="modelStore.modelForm.fields" />

                                </VaCardContent>
                            </VaCard>
                        </div>
                    </div>
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaCard>
                                <VaCardContent>
                                    <ModelIdentifier :attributes="modelStore.modelForm.fields.map(({ key }) => key)"
                                        @change="(v: any) => modelStore.modelForm.id_format = v"
                                        :model-id="modelStore.modelForm.id_format" />
                                    <ModelReference v-if="modelNames.length > 1" :models="modelNames"
                                        :reference-model="modelStore.modelForm.reference_model" :rules="[]"
                                        @change="(v: string | undefined) => modelStore.modelForm.reference_model = v">
                                    </ModelReference>
                                    <div class="row">
                                        <div class="flex lg12 md12 sm12 xs12">
                                            <VaInput style="visibility: hidden;"
                                                :rules="[(v: string) => !modelNames.includes(modelStore.modelForm.name)]">
                                            </VaInput>
                                        </div>
                                    </div>
                                </VaCardContent>
                            </VaCard>
                        </div>
                    </div>
                    <div class="row">
                        <div class="flex lg12 md12 sm12 xs12">
                            <VaButton :loading="loading" @click="submitModel">Submit</VaButton>
                        </div>
                    </div>
                </div>
            </div>
        </VaForm>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useSchemaStore } from '../../stores/schema-store';
import { useModelStore } from '../../stores/model-store';
import ModelInfo from '../../components/model/ModelInfo.vue';
import ModelAttributes from '../../components/model/ModelAttributes.vue';
import ModelIdentifier from '../../components/model/ModelIdentifier.vue';
import ModelReference from '../../components/model/ModelReference.vue';
import { useForm, useToast } from 'vuestic-ui/web-components';
import AuthService from '../../services/clients/AuthService';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';

const schemaStore = useSchemaStore()
const modelStore = useModelStore()
const { validate } = useForm('modelForm')
const router = useRouter()
const { init } = useToast()
const modelNames = computed(() => schemaStore.schema?.models.map(({ name }) => name) ?? [])

const loading = ref(false)

async function submitModel() {
    if (!schemaStore.schema) return
    const { name, version } = schemaStore.schema
    const projectId = `${name}_${version}`
    let success = false
    if (!validate()) return
    try {
        loading.value = true
        await AuthService.createModel(projectId, { ...modelStore.modelForm })
        init({ color: 'success', message: `${modelStore.modelForm.name} created` })
        success = true
    } catch (error) {
        success = false
        const axiosError = error as AxiosError
        if (axiosError.response && axiosError.response.data) {
            if (Array.isArray(axiosError.response.data)) {
                axiosError.response.data.forEach((d: string) => {
                    init({ color: 'danger', message: d })
                })
            } else {
                init({ color: 'danger', message: axiosError.response.data as string })
            }
        }
        else {
            init({ color: 'danger', message: 'Unexpected Error' })
            console.error(error)
        }
    } finally {
        loading.value = false
        if (success) {
            modelStore.resetModelForm()
            //fecth updated project
            await schemaStore.getProjectSchema(projectId)
            router.push({ name: 'projectSchema', params: { projectId } })
        }
    }

}


</script>