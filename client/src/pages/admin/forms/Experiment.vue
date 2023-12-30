<template>
    <div class="form-elements">
      <div class="row">
        <div class="flex xs12">
            <va-card :color="validExperiment?'success':'background-secondary'">
                <va-card-title>
                    Experiment Form
                </va-card-title>
                <va-card-content>
                    <va-form @validation="validExperiment = $event" ref="form">
                        <va-input class="mt-3" v-model="newExperiment.title" label="Experiment title" :rules="[value =>  Boolean(value) || 'Field is mandatory']"/>
                        <va-input type="textarea" class="mt-3" v-model="newExperiment.description" label="Experiment description"/>
                    </va-form>
                </va-card-content>
                <va-card-actions align="between">
                    <va-button @click="$refs.form.validate()">Validate Experiment</va-button>
                    <va-button color="danger" @click="$refs.form.reset()">Reset</va-button>
                </va-card-actions>
            </va-card>
        </div>
        <div class="flex xs12">
            <va-card>
                <va-card-title>
                    Biosample selection
                </va-card-title>
                <va-card-content>
                    <va-data-table
                        :items="SchemaStore.biosamples"
                        selectable
                        select-mode="multiple"
                        select-color="success"
                        @selectionChange="newExperiment.biosamples = $event.currentSelectedItems.map(it => it.name)"
                    />
                </va-card-content>
            </va-card>
        </div>
        <div class="flex xs12">
            <SchemaSelector @on-validation="validateMetadata"/>
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <va-button :disabled="!validation || !validExperiment" @click="createExperiment()">Create Experiment</va-button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
    import { ref } from 'vue'
    import {Experiment} from './types'
    import {dbStore} from '../../../stores/schemas-store'
    import SchemaSelector from '../../../components/forms/SchemaSelector.vue'
    import {useRouter} from 'vue-router'

    const validation = ref(null)
    
    const validExperiment = ref(null)

    const router = useRouter()

    const SchemaStore = dbStore()

    const newExperiment = ref<Experiment>({
        title:'',
        description:'',
        biosamples:[],
        files:[],
        schemaId:'',
        metadata:{}
    })
    function createExperiment(){
        SchemaStore.experiments.push(newExperiment.value)
        router.push({name:'dashboard'})
    }

    function validateMetadata(event, metadata){
        validation.value = event
        if(validation){
            newExperiment.value.metadata = {...metadata}
        }
    }

  </script>
  
  <style lang="scss" scoped>
    fieldset {
      margin-bottom: 0.5rem;
    }
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
  