<template>
    <div class="form-elements">
      <div class="row">
        <va-breadcrumbs>
            <va-breadcrumbs-item v-for="(br,index) in breadcrumbs" :key="index" label="One" />        </va-breadcrumbs>
        <div class="flex xs12">
            <va-inner-loading :loading="taxonInputLoading">
                <va-card>
                    <va-card-title>
                        Taxonomy Form
                    </va-card-title>
                    <Transition name="slide-fade">
                        <va-card-content key="1" v-if="!newBioSample.scientific_name">
                            <va-input v-model="newBioSample.taxid" label="NCBI Taxonomy Identifier"/>
                        </va-card-content>
                        <va-card-content key="2" v-else>
                            <p>{{ newBioSample.scientific_name }}</p>
                        </va-card-content>
                    </Transition>

                    <va-card-actions align="between">
                        <va-button :disabled="!newBioSample.taxid" @click="getTaxon(newBioSample.taxid)">Search Taxon</va-button>
                        <va-button color="danger" :disabled="!newBioSample.scientific_name" @click="resetTaxon()">Reset Taxon</va-button>
                    </va-card-actions>
                </va-card>
            </va-inner-loading>
        </div>
        <div class="flex xs12">
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
                                <va-button @click="selectSchema(schema)">select</va-button>
                            </div>
                        </div>
                    </va-card-content>
                </va-card>
                <va-card key="2" v-else>
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
                                :key="index" v-model="newBioSample.metadata[field.value]" 
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
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <va-button :disabled="!validation" @click="createBioSample()">Create BioSample</va-button>
        </div>
      </div>
      <va-modal v-model="showModal">
        <div v-for="taxon in taxons" :key="taxon.taxid">
            <div class="row justify-space-between align-center">
                <div class="flex">
                    {{ `${taxon.scientific_name} (${taxon.taxid})` }}
                </div>
                <div class="flex">
                    <va-button @click="selectTaxon(taxon)">select</va-button>
                </div>
            </div>
            <va-divider/>
        </div>
      </va-modal>
    </div>
  </template>
  
  <script setup lang="ts">
    import { reactive, ref } from 'vue'
    import { useI18n } from 'vue-i18n'
    import {Breadcrumb,BioSample,Taxon} from './types'
    import {dbStore} from '../../../stores/schemas-store'
    import NCBIClientService from '../../../services/clients/NCBIClientService'
    import SchemaSelector from '../../../components/forms/SchemaSelector.vue'

    const steps = ['organism_selection','schema_selection','metadata_form','submission']

    const validation = ref(null)

    const selectedTaxid = ref('')
    
    const selectedSchema = ref({})

    const taxonInputLoading = ref(false)

    const taxons = ref<Taxon[]>([])
    //if 2 request are done we wait 1 second before the next
    const counter = ref(0)

    const showModal = ref(false)

    const SchemaStore = dbStore()

    const newBioSample = ref<BioSample>({
        name:'',
        taxid:9606,
        scientific_name:'',
        schemaId:'',
        metadata:{}
    })
    function selectSchema(schema){
        schema.fields.forEach(field => {
            newBioSample.value.metadata[field.value] = null
        })
        selectedSchema.value = schema
    }
    function resetSchema(){
        validation.value=null
        selectedSchema.value = {}
    }
    function createBioSample(){
        SchemaStore.biosamples.push(newBioSample.value)
    }
    function resetForm(){
        Object.keys(newBioSample.value.metadata).forEach(k => {
            newBioSample.value.metadata[k] = null
        })
    }
    async function getTaxon(taxid:number){
        if(counter.value >= 2){
            setTimeout(()=>{},3000)
            counter.value = 0
        }
        try{
            taxonInputLoading.value = true           
            const {data, status} = await NCBIClientService.getTaxon(taxid)
            counter.value++
            if(status == 200){
                const taxonNodes = data.taxonomy_nodes.map(node => {
                    console.log(node)
                    return {
                        taxid: node.taxonomy.tax_id,
                        scientific_name : node.taxonomy.organism_name
                    }
                })
                taxons.value = taxons.value.concat(taxonNodes)
                console.log(taxons.value)
                taxonInputLoading.value = false           
                showModal.value = true
            }

        }
        catch (error){

            console.log(error)
            taxonInputLoading.value = false           

        }
    }
    function selectTaxon(taxon:Taxon){
        const {taxid, scientific_name} = taxon
        newBioSample.value.scientific_name = scientific_name
        newBioSample.value.taxid = taxid
        showModal.value = false
    }
    function resetTaxon(){
        newBioSample.value.scientific_name=''
        newBioSample.value.taxid=0
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
  