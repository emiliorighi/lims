<template>
    <Transition name="slide-fade">
        <va-card key="1" v-if="!selectedSchema.title">
            <va-card-title>
                Metadata Schemas
            </va-card-title>
            <va-card-content v-for="(schema,index) in SchemaStore.schemas" :key="index">
                <div class="row align-center">
                    <div class="flex">
                        <h6>{{ schema.title }}</h6>
                        <p>{{ schema.description }}</p>
                    </div>
                    <div class="flex">
                        <va-button @click="useSchema(schema)">select</va-button>
                    </div>
                </div>
            </va-card-content>
        </va-card>
        <va-card key="2" v-else>
            <va-card-title>
                {{ selectedSchema.title }}
            </va-card-title>
            <va-card-content>
                <div class="row align-center justify-space-between">
                    <div class="flex">
                        {{ selectedSchema.description }}
                    </div>
                    <div class="flex">
                        <va-button color="warning" @click="resetSchema()">Select another schema</va-button>
                    </div>
                </div>
            </va-card-content>
            <va-card-content>
                <va-form @validation="$emit('onValidation',$event, metadata)" ref="form">
                    <va-input 
                        class="mt-3" v-for="(field,index) in selectedSchema.fields" 
                        :key="index" v-model="metadata[field.value]" 
                        :label="field.label" :rules="[value => field.required ? Boolean(value) || 'Field is mandatory' : true]">
                    </va-input>
                </va-form>
            </va-card-content>
            <va-card-actions>
                <va-button @click="$refs.form.validate()">Validate Form</va-button>
                <va-button color="danger" @click="resetForm()">Reset form</va-button>
            </va-card-actions>
        </va-card>
    </Transition>
</template>
<script setup lang="ts">
    import {dbStore} from '../../stores/schemas-store'
    import { ref } from 'vue'

    const selectedSchema = ref({})

    const SchemaStore = dbStore()

    const metadata = ref({})
    const emits = defineEmits(['onValidation'])

    function useSchema(schema){
        console.log(schema)
        schema.fields.forEach(field => {
            metadata.value[field.value] = null
        })
        selectedSchema.value = {...schema}
    }
    function resetSchema(){
        emits('onValidation', null, metadata)
        selectedSchema.value = {}
    }
    function resetForm(){
        Object.keys(metadata.value).forEach(k => {
            metadata.value[k] = null
        })
    }

</script>
<style scoped>
    .slide-fade-enter-active {
    transition: all 0.3s ease-out;
    }

    .slide-fade-leave-active {
    transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
    }

    .slide-fade-enter-from,
    .slide-fade-leave-to {
    transform: translateX(20px);
    opacity: 0;
    }

</style>