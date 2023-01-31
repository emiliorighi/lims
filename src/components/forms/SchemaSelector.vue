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
        <va-card key="2">
            <va-card-title>
                {{ selectedSchema.title }}
            </va-card-title>
            <va-card-actions>
                <va-button color="danger" @click="resetSchema()">Select another schema</va-button>
            </va-card-actions>
            <va-card-content>
                {{ selectedSchema.description }}
            </va-card-content>
            <va-card-content>
                <va-form @validation="validation = $event" ref="form">
                    <va-input v-model="newBioSample.name" label="BioSample name" :rules="[ value => Boolean(value) || 'Field is mandatory']"/>
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

    const validation = ref(null)

    const SchemaStore = dbStore()

    const metadata = ref({})
    const emits = defineEmits(['onSelected'])

    function useSchema(schema){
        schema.fields.forEach(field => {
            metadata.value[field.value] = null
        })
        selectedSchema.value = schema
    }
    function resetSchema(){
        validation.value=null
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