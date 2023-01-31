<template>
    <div class="form-elements">
      <div class="row">
        <div class="flex xs12">
            <va-card>
                <va-tabs grow v-model="model">
                    <template #tabs>
                    <va-tab
                        v-for="tab in ['analysis', 'experiments']"
                        :key="tab"
                        :name="tab"
                        >
                        {{ tab }}
                        </va-tab>
                    </template>
                </va-tabs>
                <va-card-content>
                    <va-data-table
                        :items="SchemaStore[model]"
                        selectable
                        select-mode="single"
                        select-color="success"
                        @selectionChange="setObject(model, $event.currentSelectedItems)"

                    />
                </va-card-content>
            </va-card>
        </div>
        <div class="flex xs12">
            <va-card :color="validFile?'success':'background-secondary'">
                <va-card-title>
                    File Form
                </va-card-title>
                <va-card-content>
                    <va-form @validation="validFile = $event" ref="form">
                        <va-input class="mt-3" v-model="newFile.name" label="File name" :rules="[value =>  Boolean(value) || 'Field is mandatory']"/>
                        <va-input type="url" class="mt-3" v-model="newFile.url" label="File URL"/>
                        <va-input class="mt-3" v-model="newFile.type" label="File Type" placeholder="ex: CRAM,BAM,etc.."/>
                    </va-form>
                </va-card-content>
                <va-card-actions align="between">
                    <va-button @click="$refs.form.validate()">Validate File</va-button>
                    <va-button color="danger" @click="$refs.form.reset()">Reset</va-button>
                </va-card-actions>
            </va-card>
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <va-button :disabled="!validFile" @click="createFile()">Create File</va-button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
    import { reactive, ref } from 'vue'
    import {File} from './types'
    import {dbStore} from '../../../stores/schemas-store'
    import SchemaSelector from '../../../components/forms/SchemaSelector.vue'
    import {useRouter} from 'vue-router'


    const validFile = ref(null)
    
    const model = ref('experiments')

    const selectedObject = reactive({
        model:'',
        id: ''
    })
    const router = useRouter()

    const SchemaStore = dbStore()

    const newFile = ref<File>({
        url:'',
        name:'',
        type: ''
    })
    function createFile(){
        SchemaStore.files.push(newFile.value)
        console.log(selectedObject)
        console.log(SchemaStore[selectedObject.model])
        SchemaStore[selectedObject.model].filter(obj => obj.title === selectedObject.id)[0].files.push(newFile.value.name)
        router.push({name:'dashboard'})
    }

    function setObject(model, items){
        if(items.length){
            selectedObject.model = model
            selectedObject.id = items[0].title
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
  